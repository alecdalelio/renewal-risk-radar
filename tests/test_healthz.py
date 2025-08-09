"""
Tests for the health check endpoint.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthz_endpoint():
    """Test the /healthz endpoint returns correct status."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_healthz_endpoint_content_type():
    """Test the /healthz endpoint returns JSON content type."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
