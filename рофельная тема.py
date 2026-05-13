from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Главная страница
@app.route("/")
def home():
    return "Server works!"

# Эхо прикол
@app.route("/echo", methods=["POST"])
def echo():
    data = request.json

    return jsonify({
        "you_sent": data
    })

#Умножитель чисел JSONa на 5
@app.route("/sendData", methods=["POST"])
def sendData():
    data = request.json
    multiplied_data = {}
    multiplication(data)
    return jsonify(multiplied_data)

def multiplication(data):
    multiplied_data = {}
    for key, value in data.items():
        if isinstance(value, (int, float)):
            multiplied_data[key] = value * 5
        elif isinstance(value, str):
            multiplied_data[key] = value.upper()
    return multiplied_data



#Доработать потом
@app.route("/astro", methods=["POST"])
def astro():
    data = {}
    response = request.get(
        "http://api.open-notify.org/astros.json",
        json=data
    )
    return jsonify(response.json())

app.run(debug=True)