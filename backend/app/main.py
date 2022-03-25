from typing import Optional
from datetime import datetime
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from .domain import ReceivedMessages, Message

EXAMPLE_VIDEO_PATH = "app/media/kris_rant2.mp4"
EXAMPLE_AUDIO_PATH = "app/media/example-audio.mp3"

received_message: ReceivedMessages = ReceivedMessages()

start_time = None

# sentiment_queue: queue.Queue = queue.Queue(maxsize=200)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/video/")
def video_feed():
    def iterfile():
        with open(EXAMPLE_VIDEO_PATH, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.post("/message/")
async def post_message(
    username: str = Body(...),
    timestamp: int = Body(...),
    message: str = Body(...),
    startTime: int = Body(...),
):
    global start_time
    if start_time != None:
        if startTime != start_time:
            start_time = startTime
            received_message.clear()
    else:
        start_time = startTime

    print(
        "Received message: '{}' at {}".format(
            message, str(datetime.fromtimestamp(timestamp / 1000))
        )
    )
    received_message.add_message(
        Message(
            username=username,
            timestamp=timestamp,
            message_text=message,
        )
    )
    result_dict = {
        "avg_sentiment": received_message.get_avg_sentiment().__dict__,
        "timeline": received_message.get_timeline(window_size=3),
        "sentence_map": received_message.get_sentence_map(
            datetime.fromtimestamp(startTime / 1000),
            message_timestamp=datetime.fromtimestamp(timestamp / 1000),
        ),
    }
    return result_dict


# @app.websocket("/sentiment-stream/")
# async def return_sentiment(
#     websocket: WebSocket,
# ):
#     await websocket.accept()
#     while True:
#         msg = await sentiment_queue.get().__dict__
#         await websocket.send_text(msg)
