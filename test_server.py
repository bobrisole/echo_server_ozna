from server import app


client = app.test_client()


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.data == b"Server works!"

def test_echo():
    response = client.post(
        "/echo",
        json={
            "message": "hello"
        }
    )

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["you_sent"]["message"] == "hello"

def test_send_data():
    response = client.post(
        "/sendData",
        json={
            "a": 2,
            "name": "robert",
            "b": 0,
            "c": "p2p?>"
        }
    )

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["a"] == 10
    assert json_data["name"] == "ROBERT"
    assert json_data["b"] == 0
    assert json_data["c"] == "P2P?>"

