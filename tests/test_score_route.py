"""
Tests for the /score endpoint.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_score_with_samples():
    """Test the /score endpoint with sample data."""
    response = client.post("/score", json={"account_id": "ACME_CORP"})
    assert response.status_code == 200
    
    body = response.json()
    
    # Check all required fields are present
    required_fields = ["risk_score", "risk_drivers", "playbook", "comms", "metrics"]
    for field in required_fields:
        assert field in body, f"Missing required field: {field}"
    
    # Validate field types and constraints
    assert isinstance(body["risk_score"], int)
    assert 0 <= body["risk_score"] <= 100
    assert isinstance(body["risk_drivers"], list)
    assert isinstance(body["playbook"], list)
    assert isinstance(body["comms"], dict)
    assert isinstance(body["metrics"], dict)
    
    # Check comms structure
    assert "internal_slack" in body["comms"]
    assert "client_email" in body["comms"]


def test_score_with_custom_data():
    """Test the /score endpoint with custom data."""
    custom_request = {
        "account_id": "TEST_CORP",
        "usage": [
            {"date": "2025-08-01", "dau": 100, "used_seats": 50, "licensed_seats": 60}
        ],
        "tickets": [
            {"ticket_id": "T-001", "severity": 1, "created_at": "2025-08-01"}
        ],
        "notes": "Customer is very happy with the product."
    }
    
    response = client.post("/score", json=custom_request)
    assert response.status_code == 200
    
    body = response.json()
    assert body["account_id"] == "TEST_CORP"
