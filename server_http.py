from fastapi import FastAPI
from contextlib import asynccontextmanager
import hashlib
import asyncio
from utils import (multiplication, save_http_hash, websocket_reconnect_loop, send_http_hash)
ws_connection = None
local_store = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ws_connection

    asyncio.create_task(websocket_reconnect_loop())

    yield

    if ws_connection:
        await ws_connection.close()
        print("WebSocket closed")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def home_endpoint():

    return {
        "message": "Server works!"
    }


@app.post("/echo")
async def echo_endpoint(data: dict):

    return {
        "you_sent": data
    }


@app.post("/sendData")
async def send_data_endpoint(data: dict):

    if not data:
        return {"error": "JSON is empty"}

    multiplied_data = multiplication(data)
    return multiplied_data


@app.post("/hash")
async def hash_endpoint(data: dict):
    text = data["text"]
    hash_object = hashlib.sha256(text.encode()).hexdigest()

    return {
        "hash": hash_object
    }

@app.post("/sendLog")
async def send_log_endpoint(data: dict):
    save_http_hash(data, local_store, ws_connection)
    print(local_store)
    if ws_connection == None:
        return {"error": "websocket unavailable"}
    try:
        await send_http_hash(data, ws_connection)
        return {"status": "Ok"}

    except Exception as error:
        return{"error": str(error)}