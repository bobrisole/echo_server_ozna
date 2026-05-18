from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import websockets
import uvicorn
import json
import hashlib

app = FastAPI()

ws_connection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ws_connection

    ws_connection = await websockets.connect("ws://127.0.0.1:8000/ws")
    print("Connected to websocket server")

    yield
    await ws_connection.close()
    print("WebSocket closed")

app = FastAPI(lifespan=lifespan)


def multiplication(data):

    multiplied_data = {}

    for key, value in data.items():

        if isinstance(value, (int, float)):
            multiplied_data[key] = value * 5

        elif isinstance(value, str):
            multiplied_data[key] = value.upper()

        else:
            multiplied_data[key] = "ashalet"

    return multiplied_data


@app.get("/")
async def home():

    return {
        "message": "Server works!"
    }


@app.post("/echo")
async def echo(data: dict):

    return {
        "you_sent": data
    }


@app.post("/sendData")
async def send_data(data: dict):

    if not data:

        return {
            "error": "JSON is empty"
        }

    multiplied_data = multiplication(data)

    return multiplied_data
    
@app.post("/hash")
async def create_hash(data: dict):
    text = data["text"]
    hash_object = hashlib.sha256(text.encode()).hexdigest()

    return {
        "hash": hash_object
    }

@app.post("/sendLog")
async def sendLog(data: dict):
    try:
        await ws_connection.send(json.dumps(data))
        result = await ws_connection.recv()
        
        return json.loads(result)

    except Exception as error:
        return {"error": str(error)}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)