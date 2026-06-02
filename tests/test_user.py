import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_existed_user():
    # Используем существующий email из fake_db
    response = client.get("/users?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_get_nonexistent_user():
    response = client.get("/users?email=nonexistent@example.com")
    assert response.status_code == 404

def test_create_user():
    user_data = {"name": "John Doe", "email": "john@example.com"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    # API возвращает id созданного пользователя
    assert isinstance(response.json(), int)

def test_update_user():
    # В вашем API нет эндпоинта для обновления, только create, get, delete
    # Поэтому этот тест нужно пропустить или удалить
    pass

def test_delete_user():
    # Сначала создадим пользователя, потом удалим
    user_data = {"name": "ToDelete", "email": "todelete@example.com"}
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    
    # Удаляем по email
    response = client.delete("/users?email=todelete@example.com")
    assert response.status_code == 204
    
    # Проверяем, что пользователь действительно удалён
    get_response = client.get("/users?email=todelete@example.com")
    assert get_response.status_code == 404
