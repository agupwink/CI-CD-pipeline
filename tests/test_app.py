# tests/test_app.py
#
# WHY FIXTURES?
# A pytest fixture is a reusable setup function. Instead of creating a
# TestClient at the top of the file (which stays alive for every test),
# a fixture creates a fresh client for each test and tears it down after.
# This prevents one test's side effects from leaking into the next.

import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    # This fixture runs before each test that requests it.
    # TestClient starts a lightweight in-memory server — no real port needed.
    with TestClient(app) as c:
        yield c
    # After yield, the client is closed automatically (teardown).


# --- GET / ---

def test_root_status_code(client):
    """GET / should return HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_response_keys(client):
    """GET / should return both expected keys in the JSON body."""
    data = client.get("/").json()
    assert "message" in data
    assert "api_key_loaded" in data


def test_root_message_value(client):
    """GET / should return the correct welcome message."""
    data = client.get("/").json()
    assert data["message"] == "Welcome to the CI/CD demo!"


# --- GET /health ---

def test_health_status_code(client):
    """GET /health should return HTTP 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response(client):
    """GET /health should return exactly {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}
