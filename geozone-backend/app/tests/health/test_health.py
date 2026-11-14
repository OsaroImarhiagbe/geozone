from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}


def test_not_found():
    response = client.get("/api/v1/this-does-not-exist")
    assert response.status_code == 404
    assert response.json()["success"] is False