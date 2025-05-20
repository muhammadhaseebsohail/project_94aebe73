Since FastAPI is a Python framework, we use Python's built-in `unittest` module along with `fastapi.testclient.TestClient` for testing FastAPI endpoints. Here is an example of how you can write tests for a simple API endpoint.

Let's assume we have a FastAPI application with the following endpoint that returns an user by id:

`main.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

users = [
    User(id=1, name="John Doe", email="johndoe@example.com"),
    User(id=2, name="Jane Doe", email="janedoe@example.com")
]

@app.get("/user/{user_id}", response_model=User)
async def read_user(user_id: int):
    """
    Fetch user by id
    """
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
```
Now, we can write tests for this endpoint as follows:

`test_main.py`

```python
import unittest
from fastapi.testclient import TestClient

from main import app, User  # import the FastAPI instance and models

client = TestClient(app)

class TestMain(unittest.TestCase):

    def test_read_user(self):
        """
        Test the /user/{user_id} endpoint
        """

        # Test with an existing user
        response = client.get("/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "John Doe", "email": "johndoe@example.com"})

        # Test with a non-existing user
        response = client.get("/user/3")
        self.assertEqual(response.status_code, 404)
```
To run the tests, you can use the following command in the terminal:

```
python -m unittest test_main.py
```
Remember to adjust the imports and the API endpoint as needed. This is a basic example and your actual tests might require more setup or teardown procedures.