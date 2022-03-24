from typing import Optional
from datetime import datetime
import time
from fastapi import FastAPI, Body, WebSocket

app = FastAPI()


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
