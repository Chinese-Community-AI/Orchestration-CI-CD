import requests

def test_health_endpoint(api_client):
    response = requests.get(f"{api_client}/health", timeout=5)
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_get_all_todos_empty(api_client):
    response = requests.get(f"{api_client}/api/v1/todos", timeout=5)
    assert response.status_code == 200
    assert response.json() == []

def test_get_todo_not_found(api_client):
    response = requests.get(f"{api_client}/api/v1/todos/nonexistent", timeout=5)
    assert response.status_code == 404
    assert 'error' in response.json()

def test_create_todo_basic(api_client):
    todo_data = {
        'title': 'Test Todo',
        'description': 'Test Description'
    }
    response = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert response.status_code == 201
    
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'Test Todo'
    assert data['description'] == 'Test Description'
    assert data['completed'] is False 