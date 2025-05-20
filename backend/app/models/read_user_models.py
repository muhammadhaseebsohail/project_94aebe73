The provided API code includes a `GET` endpoint `/user/{user_id}` that fetches user by id. The request model isn't required for a `GET` request as it usually doesn't carry a payload, only parameters.

The response model `User` is already defined in the provided code, which includes the user's `id`, `name`, and `email`. Here is the Pydantic model for the same.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```

There's no mention of a service layer in the provided code. However, if there were one, it might look like this:

```python
from typing import Optional
from .models import User

class UserService:
    @staticmethod
    def get_user(user_id: int) -> Optional[User]:
        for user in users:
            if user.id == user_id:
                return user
        return None
```

In this case, the endpoint would call `UserService.get_user(user_id)`, and raise an `HTTPException` if the result is `None`.

Note: The list `users` and its contents are hard-coded for this example. In a real-world application, this data would typically come from a database or another type of data store.