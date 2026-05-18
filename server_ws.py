from fastapi import FastAPI, WebSocket
import json
import hashlib

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            #Получил сообщение от http сервера
            data = await websocket.receive_text()
            json_data = json.loads(data)

            #Проверяю, что в словаре есть ключ метод и свойство сендЛог
            if json_data.get("method") == "sendLog":
                                                                                            #Сохраняю содержимое data в inner_data
                inner_data = json_data.get("data")
                                                                                            #Преобразую inner_data в строку
                data_string = json.dumps(inner_data)
                                                                                            #Хэширую
                hash_result = hashlib.sha256(data_string.encode()).hexdigest()
                                                                                            #Шаблон для ответа
                response = {
                    "method": "sendLog",
                    "data": hash_result
                    }
                                                                                            #Отправляю ответ обратно http серверу
                await websocket.send_text(json.dumps(response))

#всякие ошибки
            else:
                error_response = {"error": str(error)}
                await websocket.send_text(json.dumps(error_response))
        except Exception as error:
            error_response = {"error": str(error)}
            await websocket.send_text(json.dumps(error_response))        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)