FastAPI is a Python-based framework and it doesn't support Socket.IO natively. However, Python has a powerful asynchronous library called Starlette that FastAPI is built on, and we can use it to achieve real-time communication similar to Socket.IO. 

Here's how you might build the chat API using FastAPI:

```python
from typing import List
from fastapi import FastAPI, WebSocket, Depends
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    """Message model for chat application"""
    name: str
    text: str

class MessageIn(BaseModel):
    """Input message model"""
    message: Message

class MessageOut(BaseModel):
    """Output message model includes sender details"""
    message: Message
    sender: str

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    """
    WebSocket chat endpoint
    
    Args:
        websocket (WebSocket): WebSocket connection
        username (str): username of the client
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        message_in = MessageIn(**data)
        message_out = MessageOut(message=message_in.message, sender=username)
        await websocket.send_json(message_out.dict())
```
In this code, a WebSocket connection is established at "/ws/{username}", where "{username}" is a path parameter. When the connection is established, it enters a loop where it waits for the client to send a message in JSON format. When a message is received, it is parsed into a Pydantic model `MessageIn`. Then, a `MessageOut` object is created and sent back to the client in JSON format.

Note that FastAPI doesn't have built-in support for broadcasting a message to all connected clients. If you need this functionality, you might need to manage a list of all connected WebSocket connections and iterate through them to send the message to all clients.