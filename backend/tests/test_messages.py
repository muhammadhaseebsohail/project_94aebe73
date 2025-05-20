Here is the code for the unit tests:

```python
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
import pytest

from .main import app, get_db
from .models import User, ChatMessage, ChatMessageBase

engine = create_engine("sqlite:///test_database.db")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Setup the test database
SQLModel.metadata.create_all(engine)

# Define the fixtures for the tests
@pytest.fixture
def test_user():
    return User(username="testuser", email="testuser@example.com")

@pytest.fixture
def test_message(test_user):
    return ChatMessage(user_id=test_user.id, content="Test message")

# Tests
def test_create_message(test_message):
    response = client.post("/messages/", json=test_message.dict())
    assert response.status_code == 200
    assert response.json() == test_message.dict()

def test_read_message(test_message):
    response = client.get(f"/messages/{test_message.id}")
    assert response.status_code == 200
    assert response.json() == test_message.dict()

def test_update_message(test_message):
    updated_message = ChatMessageBase(user_id=test_message.user_id, content="Updated message")
    response = client.put(f"/messages/{test_message.id}", json=updated_message.dict())
    assert response.status_code == 200
    assert response.json()["content"] == "Updated message"

def test_delete_message(test_message):
    response = client.delete(f"/messages/{test_message.id}")
    assert response.status_code == 200
    assert response.json() == test_message.dict()

def test_read_message_not_found():
    response = client.get("/messages/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}

def test_update_message_not_found():
    response = client.put("/messages/999", json=ChatMessageBase(user_id=1, content="Test").dict())
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}

def test_delete_message_not_found():
    response = client.delete("/messages/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Message not found"}
```

Here, we use the TestClient provided by FastAPI to send requests to our app. A sqlite database is used for testing, and the get_db dependency is overridden to use a testing session. Pytest fixtures are used to provide a user and a message for the tests. The tests check the HTTP status code and the JSON response body for each endpoint.