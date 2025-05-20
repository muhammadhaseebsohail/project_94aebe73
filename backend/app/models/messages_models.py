Here are the Pydantic models for request and response:

```python
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class User(UserBase):
    id: Optional[int] = None

class ChatMessageBase(BaseModel):
    user_id: int
    content: str

class ChatMessage(ChatMessageBase):
    id: Optional[int] = None
```

Here, User and ChatMessage are the Pydantic models that will be used for request validation and response formatting. The UserBase and ChatMessageBase models are used for request validation.

Next, let's create the API endpoints:

```python
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from .models import User, UserBase, ChatMessage, ChatMessageBase
from .database import SessionLocal, engine
from . import crud

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/messages/", response_model=ChatMessage)
def create_message(message: ChatMessageBase, db: Session = Depends(get_db)):
    db_message = crud.create_message(db, message)
    return db_message

@app.get("/messages/{message_id}", response_model=ChatMessage)
def read_message(message_id: int, db: Session = Depends(get_db)):
    message = crud.get_message(db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.put("/messages/{message_id}", response_model=ChatMessage)
def update_message(message_id: int, message: ChatMessageBase, db: Session = Depends(get_db)):
    db_message = crud.update_message(db, message_id=message_id, message=message)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@app.delete("/messages/{message_id}", response_model=ChatMessage)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = crud.delete_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message
```

In the code above, we are using SQLAlchemy for the database session and CRUD operations. The actual database operations are abstracted into the `crud` module. This makes the code cleaner and more maintainable.