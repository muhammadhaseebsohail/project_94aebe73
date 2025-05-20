Here is how you can write tests using `pytest` and `TestClient` from `fastapi`. We'll continue using the same example as above, where we have an endpoint that returns a user by id. 

`test_main.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app, User

client = TestClient(app)

def test_read_user_success():
    """
    Test getting a valid user
    """
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}

def test_read_user_not_found():
    """
    Test getting a non-existing user
    """
    response = client.get("/user/3")
    assert response.status_code == 404

def test_read_user_invalid_id():
    """
    Test getting a user with invalid id
    """
    response = client.get("/user/xyz")
    assert response.status_code == 422  # 422 Unprocessable Entity for data validation errors
```
This test suite includes tests for success cases (getting a valid user), error cases (getting a non-existing user), data validation (getting a user with invalid id) and an edge case (a user id that does not exist).

To run the tests, use pytest:

```
pytest test_main.py
```

Remember to adjust the imports and the API endpoint as per your application's structure. This is a basic example and your actual tests might require more setup or teardown procedures.