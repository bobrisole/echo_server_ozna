from flask import Flask, request, jsonify

app = Flask(__name__)

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

def empty_json():
    return jsonify({
        "error": "JSON is empty"
    }), 400

@app.route("/")
def home():
    return "Server works!"


@app.route("/echo", methods=["POST"])
def echo():
    data = request.json

    return jsonify({
        "you_sent": data
    })


@app.route("/sendData", methods=["POST"])
def sendData():
    data = request.json
    if not data:
        return empty_json()
    multiplied_data = multiplication(data)
    return jsonify(multiplied_data)

if __name__ == "__main__":
    app.run(debug=True)