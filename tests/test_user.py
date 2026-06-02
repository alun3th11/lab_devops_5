import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_and_get_user():
    # Создаём пользователя
    user_data = {"name": "Test User", "email": "test@example.com"}
    create_response = client.post("/api/v1/user", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()
    assert isinstance(user_id, int)
    
    # Получаем пользователя по email
    get_response = client.get("/api/v1/user?email=test@example.com")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_get_nonexistent_user():
    response = client.get("/api/v1/user?email=nonexistent@example.com")
    assert response.status_code == 404

def test_create_duplicate_user():
    # Создаём пользователя первый раз
    user_data = {"name": "Duplicate", "email": "duplicate@example.com"}
    response1 = client.post("/api/v1/user", json=user_data)
    assert response1.status_code == 201
    
    # Пытаемся создать с тем же email
    response2 = client.post("/api/v1/user", json=user_data)
    assert response2.status_code == 409  # Conflict

def test_delete_user():
    # Создаём пользователя
    user_data = {"name": "ToDelete", "email": "todelete@example.com"}
    create_response = client.post("/api/v1/user", json=user_data)
    assert create_response.status_code == 201
    
    # Удаляем пользователя
    delete_response = client.delete("/api/v1/user?email=todelete@example.com")
    assert delete_response.status_code == 204
    
    # Проверяем, что пользователь удалён
    get_response = client.get("/api/v1/user?email=todelete@example.com")
    assert get_response.status_code == 404

def test_get_user_after_delete():
    # Проверка, что после удаления пользователь действительно недоступен
    email = "test-after-delete@example.com"
    
    # Создаём
    client.post("/api/v1/user", json={"name": "Test", "email": email})
    
    # Удаляем
    client.delete(f"/api/v1/user?email={email}")
    
    # Пытаемся получить
    response = client.get(f"/api/v1/user?email={email}")
    assert response.status_code == 404
