import requests
import random
import json

def generate_random_data(number):
    data = {}
    for i in range(1, number + 1):
        data[f"number_{i}"] = random.randint(1, 10) * random.randint(1, 10)
    return data

def limit_for_generate_random_data():
    input_number = input("Введите число от 1 до 1000 для генерации данных: ")
    number = int(input_number)
    if 1 <= number <= 1000:
        return number
    else:
        print("Числло вне диапазона.")
        return limit_for_generate_random_data()

def extract_number(key):
    parts = key.split("_")
    number_string = parts[1]
    number = int(number_string)
    return number

def print_sorted_data(data):
    sorted_data = {}
    for key in sorted(data.keys(), key=extract_number):
        sorted_data[key] = data[key]
    print(json.dumps(sorted_data, indent=4)) #   Пасхалка   ,`'- o==3

data = generate_random_data(limit_for_generate_random_data())
response = requests.post(
    "http://127.0.0.1:5000/sendData",
    json=data
)

print_sorted_data(data)