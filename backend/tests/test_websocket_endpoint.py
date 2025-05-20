Here's how you might generate the unit tests for the FastAPI endpoint:

```python
from fastapi.testclient import TestClient
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect
import pytest
from typing import Any
import json
from your_module import app, MessageIn, Message


class WebSocketTestClient(TestClient):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.active_websockets = []

    def websocket_connect(self, url: str) -> WebSocket:
        ws = super().websocket_connect(url)
        self.active_websockets.append(ws)
        return ws

    def websocket_disconnect(self, ws: WebSocket) -> None:
        self.active_websockets.remove(ws)
        ws.close()

    def __exit__(self, *args: Any) -> None:
        for ws in self.active_websockets:
            try:
                self.websocket_disconnect(ws)
            except WebSocketDisconnect:
                pass
        super().__exit__(*args, **kwargs)


@pytest.fixture
def client():
    with WebSocketTestClient(app) as client:
        yield client


def test_websocket_endpoint(client):
    message = Message(name="test user", text="test message")
    message_in = MessageIn(message=message)
    message_json = json.dumps(message_in.dict())

    with client.websocket_connect("/ws/username") as websocket:
        websocket.send_text(message_json)
        data = websocket.receive_json()
        assert data["message"]["name"] == "test user"
        assert data["message"]["text"] == "test message"
        assert data["sender"] == "username"


def test_websocket_endpoint_no_message_text(client):
    message = Message(name="test user", text="")
    message_in = MessageIn(message=message)
    message_json = json.dumps(message_in.dict())

    with client.websocket_connect("/ws/username") as websocket:
        websocket.send_text(message_json)
        data = websocket.receive_json()
        assert data["message"]["name"] == "test user"
        assert data["message"]["text"] == ""
        assert data["sender"] == "username"


def test_websocket_endpoint_no_message_name(client):
    message = Message(name="", text="test message")
    message_in = MessageIn(message=message)
    message_json = json.dumps(message_in.dict())

    with client.websocket_connect("/ws/username") as websocket:
        websocket.send_text(message_json)
        data = websocket.receive_json()
        assert data["message"]["name"] == ""
        assert data["message"]["text"] == "test message"
        assert data["sender"] == "username"


def test_websocket_endpoint_no_username(client):
    message = Message(name="test user", text="test message")
    message_in = MessageIn(message=message)
    message_json = json.dumps(message_in.dict())

    with client.websocket_connect("/ws/") as websocket:
        websocket.send_text(message_json)
        data = websocket.receive_json()
        assert data["message"]["name"] == "test user"
        assert data["message"]["text"] == "test message"
        assert data["sender"] == ""
```

In these tests, a `WebSocketTestClient` class is created to manage WebSocket connections during testing. It stores all active connections in a list and closes them when the client is exited. This class is used in a pytest fixture to make it available to all test functions.

In the `test_websocket_endpoint` function, a `MessageIn` object is created and sent over the WebSocket connection. The response is then checked to ensure that it contains the correct data. 

The `test_websocket_endpoint_no_message_text`, `test_websocket_endpoint_no_message_name`, and `test_websocket_endpoint_no_username` tests are similar, but they test edge cases where one of the fields is an empty string.