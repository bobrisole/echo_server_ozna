import json
import hashlib
import asyncio
import websockets

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
            print(local_store)

    return

async def save_http_hash(data, local_store: list, ws_connection):
    inner_data = data["data"]
    hash_value = create_hash(inner_data)
    local_store.append({
        "data": inner_data,
        "hash": hash_value})

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
            print(f"Listener ERROR: {e}")
            break

async def websocket_reconnect_loop():
    import server_http

    while True:

        try:
            server_http.ws_connection = await websockets.connect("ws://127.0.0.1:8000/ws")
            print("WS CONNECTED √           ")

            await websocket_listener(server_http.ws_connection,server_http.local_store)

        except Exception:
            print("", end = '')

        finally:
            server_http.ws_connection = None

            for i in range(5, 0, -1):
                print(f"TRYING RECONNECT TO WS AFTER {i} SEC",end="\r")
                await asyncio.sleep(1)
