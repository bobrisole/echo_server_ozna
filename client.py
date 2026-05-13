import requests
import random

data = {}
for number in range(1, 1001):
    data[f"number_{number}"] = random.randint(1, 10) * random.randint(1, 10)

# Отправляем POST-запрос
response = requests.post(
    "http://127.0.0.1:5000/sendData",
    json=data
)

print(response.json())