Here is how you might implement a user authentication API with login/logout endpoints and JWT using FastAPI and Python:

First, we need to install the required libraries:
```python
pip install fastapi pydantic python-jose[cryptography] passlib[bcrypt] python-multipart
```

```python
# imports
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# secret key for JWT creation - this should be secret and complex in real applications
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fastapi app
app = FastAPI()

# Pydantic models
class User(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# this would be replaced with a real database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": pwd_context.hash("secret"),
    }
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    return {"detail": "Logout successful"}
```

In this code, we use FastAPI's OAuth2PasswordRequestForm for the login endpoint. The password is hashed with bcrypt and stored in a fake database. When a user logs in, the password is checked and if it's valid, a JWT token is returned. The logout endpoint doesn't do much currently but in a real-world scenario, it could invalidate the user's token.

The JWT token is created with the help of python-jose library. It's encoded with the user's username and an expiration time. In a real-world application, the secret key should be kept secret and it should be complex. 

The token is then used for authenticating the user in subsequent requests. The authentication could be implemented with the help of a dependency that checks if the token is valid.