from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_existing_user():
    response = client.get("/users/2")

    assert response.status_code == 200


def test_get_non_existing_user():
    response = client.get("/users/99999")

    assert response.status_code == 404
    assert response.json() == {"error": "User not found"}