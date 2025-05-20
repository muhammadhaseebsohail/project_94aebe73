To complete this task, we'll use SQLModel, which is a library for interacting with SQL databases in Python that combines the features of SQLAlchemy and Pydantic. 

Here are the steps:
1. Define the User and ChatMessage models
2. Create a router with CRUD operations for ChatMessage

First, let's set up the database models:

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str
    email: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ChatMessageBase(SQLModel):
    user_id: int
    content: str

class ChatMessage(ChatMessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```

Here, User and ChatMessage are the SQLModel classes that will be translated into SQL tables. The UserBase and ChatMessageBase models are used for request validation.

Next, let's create the API endpoints:

```python
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, SQLModel, create_engine, select
from .models import ChatMessage, ChatMessageBase, User

engine = create_engine("sqlite:///database.db")

app = FastAPI()

# Dependency
def get_db():
    with Session(engine) as session:
        yield session

@app.post("/messages/", response_model=ChatMessage)
def create_message(message: ChatMessageBase, db: Session = Depends(get_db)):
    """
    Create a new chat message.
    """
    db_message = ChatMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/{message_id}", response_model=ChatMessage)
def read_message(message_id: int, db: Session = Depends(get_db)):
    """
    Get a specific chat message by id.
    """
    message = db.get(ChatMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.put("/messages/{message_id}", response_model=ChatMessage)
def update_message(message_id: int, message: ChatMessageBase, db: Session = Depends(get_db)):
    """
    Update a chat message by id.
    """
    db_message = db.get(ChatMessage, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    for key, value in message.dict().items():
        setattr(db_message, key, value)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.delete("/messages/{message_id}", response_model=ChatMessage)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    """
    Delete a chat message by id.
    """
    message = db.get(ChatMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return message
```

Here, we have four API endpoints for creating, reading, updating, and deleting chat messages. The get_db function is a dependency that provides a database session for each request. It's used in FastAPI's Depends function to inject a database session into each endpoint.