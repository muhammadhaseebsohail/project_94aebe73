Here is how you can implement the unit tests for the FastAPI endpoint using pytest and FastAPI's TestClient:

```python
# imports
from fastapi.testclient import TestClient
import pytest
from main import app, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

# setup the test client
client = TestClient(app)

# test data
user = {"username": "johndoe", "password": "secret"}
invalid_user = {"username": "johndoe", "password": "invalid_password"}

def test_authenticate_user():
    assert authenticate_user("johndoe", "secret") == user
    assert authenticate_user("johndoe", "invalid_password") == None

def test_create_access_token():
    data = {"sub": user['username']}
    access_token = create_access_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    assert access_token is not None

def test_login_for_access_token_success():
    response = client.post("/token", data=user)
    assert response.status_code == 200
    assert "access_token" in response.json() 
    assert "token_type" in response.json()

def test_login_for_access_token_fail():
    response = client.post("/token", data=invalid_user)
    assert response.status_code == 401
    assert "detail" in response.json()

def test_logout():
    # first login to get a token
    response = client.post("/token", data=user)
    token = response.json().get("access_token")
    # then logout
    response = client.get("/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"detail": "Logout successful"}

def test_logout_without_token():
    response = client.get("/logout")
    assert response.status_code == 403
```

These tests cover:
- Success cases: successful authentication, token creation, login, and logout
- Error cases: failed login due to incorrect password, and logout attempt without a token
- Data validation: checks that the responses contain the expected data
- Edge cases: login with invalid credentials, and logout without a token.