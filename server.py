from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/echo", methods=["POST"])
def echo():
    data = request.json

    return jsonify({
        "you_sent": data
    })

@app.route("/")
def home():
    return "Server works!"

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}"

app.run(debug=True)