import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_existed_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_nonexistent_user():
    response = client.get("/users/99999")
    assert response.status_code == 404

def test_create_user():
    user_data = {"name": "John Doe", "email": "john@example.com"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]

def test_update_user():
    updated_data = {"name": "Jane Smith"}
    response = client.patch("/users/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Smith"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 204
