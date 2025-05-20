As per your request, here are the code snippets including the necessary Pydantic models, endpoint code, service layer code, and imports. 

1. Pydantic Models for request/response:

```python
from pydantic import BaseModel, Field

class DeploymentRequest(BaseModel):
    """
    Model representing a request to deploy an application.
    """
    server_id: str = Field(..., description="The ID of the server to deploy on.")
    docker_image: str = Field(..., description="The Docker image to deploy.")


class DeploymentResponse(BaseModel):
    """
    Model representing a response from a deployment request.
    """
    success: bool = Field(..., description="Whether the deployment was successful.")
    message: str = Field(..., description="A message describing the result of the deployment.")
```

2. Endpoint code with all imports:

```python
from fastapi import FastAPI, HTTPException
from .models import DeploymentRequest, DeploymentResponse
from .services import deploy_application

app = FastAPI()

@app.post("/deploy", response_model=DeploymentResponse, status_code=201)
def deploy_application_endpoint(request: DeploymentRequest):
    """
    Deploy an application to a server.

    This endpoint takes a DeploymentRequest and returns a DeploymentResponse.

    :param request: The deployment request.
    :return: The result of the deployment.
    """
    try:
        response = deploy_application(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during deployment.") from e
```

3. Service layer code:

```python
def deploy_application(request: DeploymentRequest) -> DeploymentResponse:
    """
    Deploy an application to a server.
    
    This function is a stub and needs to be implemented.

    :param request: The deployment request.
    :return: The result of the deployment.
    """
    # TODO: Implement this function.
    return DeploymentResponse(success=True, message="Deployment successful.")
```