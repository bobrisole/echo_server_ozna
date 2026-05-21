from fastapi import FastAPI, WebSocket
import json
from utils_ws import send_ws_hash


app = FastAPI()


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        try:
            raw = await ws.receive_text()
            message = json.loads(raw)

            if message.get("method") == "sendLog":
                await send_ws_hash(ws, message)
            else:
                print("UNKNOWN METHOD")
                await ws.send_text(json.dumps({"error": "unknown method"}))

        except Exception as error:

            print(error)
            await ws.send_text(json.dumps({"error": str(error)}))