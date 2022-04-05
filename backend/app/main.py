from typing import Optional
from datetime import datetime
from fastapi import FastAPI, Body, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from .domain import ReceivedMessages, Message
from threading import Timer
from typing import List
import json

EXAMPLE_VIDEO_PATH = "app/media/kris_rant2.mp4"
EXAMPLE_AUDIO_PATH = "app/media/example-audio.mp3"

received_message: ReceivedMessages = ReceivedMessages()

send_messages = []

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

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/messages")
def read_messages():
    return send_messages

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
    # startTime: int = Body(...),
):
    # global start_time
    # if start_time != None:
    #     if startTime != start_time:
    #         start_time = startTime
    #         received_message.clear()
    # else:
    #     start_time = startTime

    message = message.strip()
    username = username.strip()

    if message == '' or username == '':
       return

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
        # "sentence_map": received_message.get_sentence_map(
        #     datetime.fromtimestamp(startTime / 1000),
        #     message_timestamp=datetime.fromtimestamp(timestamp / 1000),
        # ),
    }

    result = {
        "message": {
            "username": username,
            "timestamp": timestamp,
            "message": message,
        },
        "result": result_dict
    }
    # print(result)

    send_messages.append({
      "username": username,
      "timestamp": timestamp,
      "message": message,
    })

    await manager.broadcast(
        str(json.dumps(result)))
    # await manager.broadcast("HEY")

    return result_dict


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     # connections.append(MyWebSocket(websocket))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #hello says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #hello left the chat")


@app.get("/mock/reset-messages")
def send_mock_message_request():
    received_message.clear()
    send_messages.clear()
    return

@app.get("/mock/messages")
def send_mock_message_request():
    send_mock_message()
    return

def send_mock_message():
    
    for i in range(0, 129):
        result = list(filter(lambda x: x["timestamp"] == i, messages))
        # print(i, result)
        for m in result:
            print(i, m)


messages = [{
   "message":"Hi, FIRST!",
   "timestamp":1,
   "username":"elrak"
},
{
   "message":"Hey 😀😀😀😀😀😀😀😀😀",
   "timestamp":1,
   "username":"proGamerLPHD"
},
{
   "message":"😀😀😀y",
   "timestamp":1,
   "username":"yoloTV"
},
{
   "message":"YOOYOYOYOYOOYYO",
   "timestamp":1,
   "username":"FifaPro2008"
},
{
   "message":"Moin",
   "timestamp":2,
   "username":"germanLetsplayer"
},
{
   "message":"Heyyyyyyy, heyyyy",
   "timestamp":2,
   "username":"proGamerLPHD"
},
{
   "message":"Hi Kriiis ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️",
   "timestamp":2,
   "username":"zuluuuuu"
},
{
   "message":"Bro",
   "timestamp":3,
   "username":"footballguy12"
},
{
   "message":"🆒🆒🆒🆒🆒🆒🆒🆒🆒🆒🆒",
   "timestamp":4,
   "username":"proGamerLPHD"
},
{
   "message":"💩💩💩💩💩💩💩💩💩💩💩💩",
   "timestamp":5,
   "username":"gamer12"
},
{
   "message":"FIFA FIFA",
   "timestamp":10,
   "username":"ronaldo56"
},
{
   "message":"GOOOOOOOOOOOOOOOOO",
   "timestamp":6,
   "username":"ChessLegendChess"
},
{
   "message":"Hey Kris 😎",
   "timestamp":8,
   "username":"Marcel#1337"
},
{
   "message":"Hiii",
   "timestamp":9,
   "username":"jkfklofsds"
},
{
   "message":"😎😎😎😎😎😎😎😎😎😎😎😎",
   "timestamp":10,
   "username":"TheDoooooor543"
},
{
   "message":"Hi Kris let's win some games",
   "timestamp":12,
   "username":"DesignRuben69"
},
{
   "message":"🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸🥸",
   "timestamp":14,
   "username":"Marcel#1337"
},
{
   "message":"Today it is raining",
   "timestamp":12,
   "username":"umbrellaMan1000"
},
{
   "message":"START HACK!!!!!!!",
   "timestamp":14,
   "username":"Daniel"
},
{
   "message":"🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡🤡",
   "timestamp":13,
   "username":"proGamerLPHD"
},
{
   "message":"Let's play clash royal",
   "timestamp":19,
   "username":"ML_Alex007"
},
{
   "message":"Ultimate TEAM",
   "timestamp":20,
   "username":"umbrellaMan1000"
},
{
   "message":"⚽⚽⚽⚽⚽⚽⚽",
   "timestamp":21,
   "username":"ronaldo56"
},
{
   "message":"accept my firend request",
   "timestamp":21,
   "username":"DesignRuben69"
},
{
   "message":"FIFA",
   "timestamp":22,
   "username":"proGamerLPHD"
},
{
   "message":"Kris is the best",
   "timestamp":24,
   "username":"KRISFAN2013"
},
{
   "message":"This guy is hacking!!!!!!!!!",
   "timestamp":26,
   "username":"NotAHacker123"
},
{
   "message":"Clash royal > FIFA",
   "timestamp":28,
   "username":"supercellfan34"
},
{
   "message":"Shoot",
   "timestamp":30,
   "username":"gamer12"
},
{
   "message":"⚽⚽⚽⚽⚽⚽⚽⚽⚽⚽",
   "timestamp":32,
   "username":"KRISFAN2013"
},
{
   "message":"Yes he is!",
   "timestamp":37,
   "username":"ronaldo56"
},
{
   "message":"Troll!",
   "timestamp":39,
   "username":"NotAHacker123"
},
{
   "message":"Nice play!",
   "timestamp":44,
   "username":"gamer12"
},
{
   "message":"Hi Krisman!!!",
   "timestamp":48,
   "username":"Baker494"
},
{
   "message":"Get the ball!",
   "timestamp":52,
   "username":"KRISFAN2013"
},
{
   "message":"This was a goal!!!",
   "timestamp":55,
   "username":"supercellfan34"
},
{
   "message":"You are bad!",
   "timestamp":57,
   "username":"NotAHacker123"
},
{
   "message":"😈😈😈😈😈😈😈😈",
   "timestamp":58,
   "username":"ML_Alex007"
},
{
   "message":"Drink some water man!",
   "timestamp":59,
   "username":"waterman"
},
{
   "message":"Long live the lost ball",
   "timestamp":60,
   "username":"Tomuchsad"
},
{
   "message":"Chill",
   "timestamp":62,
   "username":"KRISFAN2013"
},
{
   "message":"For sure!",
   "timestamp":64,
   "username":"gamer12"
},
{
   "message":"🥶🥶🥶🥶",
   "timestamp":64,
   "username":"DesignRuben69"
},
{
   "message":"GO Sports!",
   "timestamp":68,
   "username":"proGamerLPHD"
},
{
   "message":"I really enjoy your entertaining content",
   "timestamp":72,
   "username":"StreamLover99"
},
{
   "message":"Whoah, that not cool! You went too far there. That was shit!",
   "timestamp":76,
   "username":"Hackerman123"
},
{
   "message":"Yeah that was really uncalled for!",
   "timestamp":77,
   "username":"StreamLover99"
},
{
   "message":"NOOOOOOO",
   "timestamp":78,
   "username":"BigBear43"
},
{
   "message":"Dont be mean!",
   "timestamp":79,
   "username":"StreamLover99"
},
{
   "message":"That is bad!",
   "timestamp":79,
   "username":"StreamLover99"
},
{
   "message":"Dont insult",
   "timestamp":83,
   "username":"BigBear43"
},
{
   "message":"It is just a game, no need to insult people!",
   "timestamp":80,
   "username":"BigBear43"
},
{
   "message":"WHAT",
   "timestamp":82,
   "username":"BigBear43"
},
{
   "message":"Dont insult",
   "timestamp":83,
   "username":"BigBear43"
},
{
   "message":"It is just a game, no need to insult people!",
   "timestamp":83,
   "username":"BigBear43"
},
{
   "message":"Thats not!",
   "timestamp":83,
   "username":"BigBear43"
},
{
   "message":"bad",
   "timestamp":85,
   "username":"BigBear43"
},
{
   "message":";(",
   "timestamp":85,
   "username":"BigBear43"
},
{
   "message":"OK",
   "timestamp":88,
   "username":"PRFGUY"
},
{
   "message":"Well, done! Nice Goal",
   "timestamp":95,
   "username":"StreamLover99"
},
{
   "message":"Damn man! What a superb shot",
   "timestamp":96,
   "username":"BigBear43"
},
{
   "message":"That showed some great skill! I love you!",
   "timestamp":97,
   "username":"StreamLover99"
},
{
   "message":"Thats a nice attitude!",
   "timestamp":98,
   "username":"Hackerman123"
},
{
   "message":"Yeah he sadly really is not the best player :/",
   "timestamp":108,
   "username":"StreamLover99"
},
{
   "message":"Maybe you could teach him some of your tricks :)",
   "timestamp":109,
   "username":"Hackerman123"
},
{
   "message":"Well then go ahead and win this game!",
   "timestamp":117,
   "username":"BigBear43"
},
{
   "message":"Indeed maybe you are not as good as you thought after all",
   "timestamp":122,
   "username":"MoSalah65"
},
{
   "message":"No Kris is the best player in the world!",
   "timestamp":123,
   "username":"StreamLover99"
},
{
   "message":"Congratulations on the nice game!",
   "timestamp":128,
   "username":"Hackerman123"
},
{
   "message":"GG! Well played!",
   "timestamp":129,
   "username":"StreamLover99"
},

]