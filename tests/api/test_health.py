"""
API tests for the health check endpoint.
"""
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

# The TestClient allows us to make HTTP requests to our FastAPI app in tests
client = TestClient(app)

def test_health_check():
    """
    Tests the GET /api/v1/health/ endpoint.
    It should return a 200 OK status and the correct JSON body.
    """
    # 1. Make a request to the endpoint
    response = client.get("/api/v1/")

    # 2. Assert the HTTP status code
    assert response.status_code == status.HTTP_200_OK

    # 3. Assert the response body content
    assert response.json() == {"status": "ok"}
