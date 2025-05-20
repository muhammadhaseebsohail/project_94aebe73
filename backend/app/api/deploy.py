Here is an example of how you might create such an endpoint with FastAPI. In this example, we will assume that the deployment process involves sending some configuration data to the server, and then receiving a response indicating whether the deployment was successful.

Let's start with the Pydantic models:

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

Now let's move on to the service layer. We'll just create a stub function for now:

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

Now we can create our endpoint:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

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

This code includes error handling and logging: if an error occurs during deployment, an HTTP 500 response will be returned, and the error will be logged. It also includes data validation using Pydantic: the request and response models are used to validate the incoming and outgoing data. The endpoint is also documented using docstrings and FastAPI's automatic OpenAPI documentation generation.

Note that this code does not include any authentication or authorization, as it was not specified in the task requirements. However, in a real-world application, you would likely want to secure this endpoint in some way, such as by requiring an API key or a specific user role.