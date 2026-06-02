import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.anyio
async def test_get_existed_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/1")
    assert response.status_code == 200
    assert "id" in response.json()

async def test_get_nonexistent_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/99999")
    assert response.status_code == 404

async def test_create_user():
    user_data = {"name": "John Doe", "email": "john@example.com"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]

async def test_update_user():
    updated_data = {"name": "Jane Smith"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch("/users/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Smith"

async def test_delete_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/users/1")
    assert response.status_code == 204
