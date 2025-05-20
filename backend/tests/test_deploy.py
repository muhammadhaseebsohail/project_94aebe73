Sure, here's how you can write comprehensive unit tests for the FastAPI endpoint using pytest and FastAPI's TestClient:

```python
from fastapi.testclient import TestClient
import pytest
from main import app, DeploymentRequest, DeploymentResponse, deploy_application 

client = TestClient(app)

def test_deploy_application_success():
    """
    Test successful deployment
    """
    deployment_request = DeploymentRequest(server_id="123", docker_image="my-app:latest")
    response = client.post("/deploy", json=deployment_request.dict())
    assert response.status_code == 201
    assert response.json() == {"success": True, "message": "Deployment successful."}

def test_deploy_application_failure():
    """
    Test failed deployment
    """
    deployment_request = DeploymentRequest(server_id="123", docker_image="my-app:latest")
    # Mock the deploy_application function to always raise an exception
    app.dependency_overrides[deploy_application] = lambda x: 1/0
    response = client.post("/deploy", json=deployment_request.dict())
    assert response.status_code == 500
    assert response.json() == {"detail": "An error occurred during deployment."}
    # Remove the mock to not affect other tests
    app.dependency_overrides = {}

@pytest.mark.parametrize("payload", [
    {"server_id": "123"},  # missing docker_image
    {"docker_image": "my-app:latest"},  # missing server_id
    {},  # missing both server_id and docker_image
])
def test_deploy_application_invalid_data(payload):
    """
    Test deployment with invalid data
    """
    response = client.post("/deploy", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_deploy_application_edge_case():
    """
    Test deployment with edge case data
    """
    deployment_request = DeploymentRequest(server_id="   ", docker_image="   ")
    response = client.post("/deploy", json=deployment_request.dict())
    assert response.status_code == 422  # Unprocessable Entity
```

Here, we're testing a successful deployment, a failed deployment (by mocking the deploy_application function to always raise an exception), invalid data (missing required fields), and an edge case (where the required fields are present but only contain whitespace).