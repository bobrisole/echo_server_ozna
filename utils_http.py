import json
import hashlib
import asyncio
import websockets
from datetime import datetime, UTC
from utils_http_storage import save_local_store
import time


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

def create_hash(data: dict):
    normalized = json.dumps(data,sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()

def find_and_remove_matches(local_store: list,server_hashes: list):

    for item in local_store:
        if item["hash"] in server_hashes:
            local_store.remove(item)
            save_local_store(local_store)
            print(f"Local Store after removal: {local_store}")

async def save_http_hash(data, local_store: list):
    inner_data = data["data"]
    hash_value = create_hash(inner_data)
    local_store.append({
        "data": inner_data,
        "hash": hash_value,
        "last_try": time.monotonic(),
        "YMD": datetime.now(UTC).isoformat()})
    save_local_store(local_store)

    print(f"Local Store: {local_store}")

async def send_http_hash(data, ws_connection):
        try:
            await ws_connection.send(json.dumps(data))
        except Exception as e:
            print(f"Error sending data over WebSocket: {e}")

async def websocket_listener(ws_connection, local_store):
    while True:
        try:
            response = json.loads(await ws_connection.recv())
            method = response.get("method")

            if method == "sendHash":
                server_hashes = response.get("ws_hash", [])
                find_and_remove_matches(local_store,server_hashes)

            elif method == "ping":
                print("PING RECEIVED")

            else:
                print("UNKNOWN METHOD")

        except Exception as e:
            print(f"WebSocket disconnected: {e}")
            break

async def websocket_reconnect_loop():

    import server_http

    while True:

        try:
            server_http.ws_connection = await websockets.connect("ws://127.0.0.1:8000/ws")
            print("WS CONNECTED TO SERVER..√           ")
            await websocket_listener(server_http.ws_connection,server_http.local_store)

        except Exception as e:
            print("", end = '')

        finally:
            server_http.ws_connection = None

            for i in range(5, 0, -1):
                print(f"TRYING RECONNECT TO WS AFTER {i} SEC",end="\r")
                await asyncio.sleep(1)

async def historical_send(ws_connection, local_store):

    if ws_connection and len(local_store) > 0:
        for item in local_store:
            try:
                await ws_connection.send(json.dumps({"method": "sendLog", "data": item["data"]}))
            except Exception as e:
                print(f"Error in historical_send: {e}")

async def retry_old_logs():
    import server_http
    while True:
        try:
            now = time.monotonic()

            for item in server_http.local_store[:]:
                last_try = item["last_try"]
                if abs(now - last_try) > 15:
                    print("RETRY:", item)

                    await server_http.ws_connection.send(
                        json.dumps({
                            "method": "sendLog",
                            "data": item["data"]})
                    )
                    item["last_try"] = now

        except Exception as error:
            print("RETRY ERROR:", error)

        await asyncio.sleep(15)