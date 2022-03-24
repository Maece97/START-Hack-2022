from typing import Optional
from datetime import datetime
import time
from fastapi import FastAPI, Body, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://start-hack-2022-xertbtzkda-uc.a.run.app",
    "https://start-hack-2022-xertbtzkda-uc.a.run.app",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.websocket("/sentiment-stream")
async def return_sentiment(
        websocket: WebSocket,
):
    await websocket.accept()
    while True:
        result = {"result": 0.23}
        await websocket.send_text(result)
        time.sleep(10)
