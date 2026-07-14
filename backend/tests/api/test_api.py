import pytest

def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_get_profile_unauthorized(client):
    response = client.get("/api/v1/users/profile")
    assert response.status_code == 401

def test_get_profile_authorized(auth_client):
    response = auth_client.get("/api/v1/users/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["username"] == "admin_test"
