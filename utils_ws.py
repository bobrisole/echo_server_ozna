import json
import hashlib
from datetime import datetime, UTC
import time

def create_hash(data: dict):
    normalized = json.dumps(data,sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()

async def send_ws_hash(ws, message):
    data = message["data"]
    hash_value = create_hash(data)
    response = {
        "method": "sendHash",
        "ws_hash": [hash_value],
        "last_try": time.monotonic(),
        "YMD": datetime.now(UTC).isoformat()}
    
    print(f"Sending hash over WebSocket: {response}")
    await ws.send_text(json.dumps(response))