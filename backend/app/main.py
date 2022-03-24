from typing import Optional
from datetime import datetime
import time
from fastapi import FastAPI, Body, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

EXAMPLE_VIDEO_PATH = "example-video.mp4"

def create_app() -> CORSMiddleware:
    """Create app wrapper to overcome middleware issues."""
    fastapi_app = FastAPI()
    return CORSMiddleware(
        fastapi_app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}



@app.post("/message/")
def post_message(
        timestamp: int = Body(...), message: str = Body(...)
):
    timestr = str(datetime.fromtimestamp(timestamp))  
    print("Received message: '{}' at {}".format(message, timestr) )
    return 


@app.get("/video/")
def video_feed():
    def iterfile():  
        with open(EXAMPLE_VIDEO_PATH, mode="rb") as file_like: 
            yield from file_like 
    return StreamingResponse(iterfile(), media_type="video/mp4")


@app.websocket("/sentiment-stream/")
async def return_sentiment(
        websocket: WebSocket,
):
    await websocket.accept()
    while True:
        result = {"result": 0.23}
        await websocket.send_text(result)
        time.sleep(10)
