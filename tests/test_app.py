# tests/test_app.py
#
# These are automated tests for the FastAPI app.
#
# WHY TEST?
# When you change code, tests automatically verify that existing features
# still work. Without tests, you have to manually click through the app
# every time — which gets tedious and error-prone as the project grows.
#
# HOW IT WORKS:
# FastAPI's TestClient sends real HTTP requests to the app without starting
# a server. It's fast, requires no network, and works inside GitHub Actions.

from fastapi.testclient import TestClient
from app import app

# Create a test client that talks directly to our FastAPI app.
client = TestClient(app)


def test_root_status_code():
    """GET / should return HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_response_keys():
    """GET / should return both expected keys in the JSON body."""
    response = client.get("/")
    data = response.json()
    assert "message" in data
    assert "api_key_loaded" in data


def test_root_message_value():
    """GET / should return the correct welcome message."""
    response = client.get("/")
    assert response.json()["message"] == "Welcome to the CI/CD demo!"


def test_health_status_code():
    """GET /health should return HTTP 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response():
    """GET /health should return {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}
