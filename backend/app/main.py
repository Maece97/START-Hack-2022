from typing import Optional
from datetime import datetime
import time
from fastapi import FastAPI, Body, WebSocket
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

EXAMPLE_VIDEO_PATH = "app/example-video.mp4"

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
def post_message(
    username: str = Body(), timestamp: int = Body(...), message: str = Body(...)
):
    timestr = str(datetime.fromtimestamp(timestamp))
    print("Received message: '{}' at {}".format(message, timestr))
    return


@app.websocket("/sentiment-stream/")
async def return_sentiment(
    websocket: WebSocket,
):
    await websocket.accept()
    while True:
        result = {"result": 0.23}
        await websocket.send_text(result)
        time.sleep(10)
