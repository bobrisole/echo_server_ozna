import json
import hashlib


def create_hash(data: dict):
    normalized = json.dumps(data,sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()

async def send_ws_hash(ws, message):
    data = message["data"]
    hash_value = create_hash(data)
    response = {
        "method": "sendHash",
        "ws_hash": [hash_value]
    }
    await ws.send_text(json.dumps(response))