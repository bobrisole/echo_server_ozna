from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    print("CONNECTED")

    while True:

        data = await websocket.receive_text()

        print("DATA:", data)

        await websocket.send_text(data)