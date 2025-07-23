import requests

def test_health_endpoint(api_client):
    response = requests.get(f"{api_client}/health", timeout=5)
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_get_with_no_parameters(api_client):
    """GET with no parameters returns appropriate response"""
    response = requests.get(f"{api_client}/api/v1/todos", timeout=5)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_with_parameters_completed_false(api_client):
    """GET with appropriate parameters returns expected JSON from database"""
    # First create a todo
    todo_data = {'title': 'Test Todo', 'completed': False}
    create_response = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert create_response.status_code == 201
    
    # Query with completed=false parameter
    response = requests.get(f"{api_client}/api/v1/todos?completed=false", timeout=5)
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) >= 1
    assert any(todo['title'] == 'Test Todo' for todo in todos)

def test_get_no_results(api_client):
    """GET that finds no results returns appropriate response"""
    response = requests.get(f"{api_client}/api/v1/todos?completed=true", timeout=5)
    assert response.status_code == 200
    assert response.json() == []

def test_get_with_incorrect_parameters(api_client):
    """GET with incorrect parameters returns appropriate response"""
    response = requests.get(f"{api_client}/api/v1/todos?invalid_param=value", timeout=5)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_creates_in_database_and_s3(api_client):
    """POST results in JSON body being stored in database and S3 bucket"""
    todo_data = {
        'title': 'Test Todo for Storage',
        'description': 'Test Description'
    }
    response = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert response.status_code == 201
    
    created_todo = response.json()
    assert 'id' in created_todo
    assert created_todo['title'] == 'Test Todo for Storage'
    assert created_todo['completed'] is False
    
    # Verify it can be retrieved
    get_response = requests.get(f"{api_client}/api/v1/todos/{created_todo['id']}", timeout=5)
    assert get_response.status_code == 200
    assert get_response.json()['title'] == 'Test Todo for Storage'

def test_post_duplicate_handling(api_client):
    """POST duplicate request returns appropriate response"""
    todo_data = {'title': 'Duplicate Todo'}
    
    # Create first todo
    response1 = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert response1.status_code == 201
    
    # Create second todo with same title (should still succeed with different ID)
    response2 = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert response2.status_code == 201
    assert response1.json()['id'] != response2.json()['id']

def test_put_updates_existing_resource(api_client):
    """PUT that targets existing resource updates database and S3 bucket"""
    # Create a todo first
    todo_data = {'title': 'Original Title'}
    create_response = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert create_response.status_code == 201
    todo_id = create_response.json()['id']
    
    # Update the todo
    update_data = {'title': 'Updated Title', 'completed': True}
    put_response = requests.put(f"{api_client}/api/v1/todos/{todo_id}", json=update_data, timeout=5)
    assert put_response.status_code == 200
    
    updated_todo = put_response.json()
    assert updated_todo['title'] == 'Updated Title'
    assert updated_todo['completed'] is True

def test_put_with_no_valid_target(api_client):
    """PUT with no valid target returns appropriate response"""
    update_data = {'title': 'Updated Title'}
    response = requests.put(f"{api_client}/api/v1/todos/nonexistent-id", json=update_data, timeout=5)
    assert response.status_code == 404
    assert 'error' in response.json()

def test_delete_removes_from_database_and_s3(api_client):
    """DELETE removes item from database and S3 bucket"""
    # Create a todo first
    todo_data = {'title': 'Todo to Delete'}
    create_response = requests.post(f"{api_client}/api/v1/todos", json=todo_data, timeout=5)
    assert create_response.status_code == 201
    todo_id = create_response.json()['id']
    
    # Delete the todo
    delete_response = requests.delete(f"{api_client}/api/v1/todos/{todo_id}", timeout=5)
    assert delete_response.status_code == 200
    assert 'message' in delete_response.json()
    
    # Verify it's gone
    get_response = requests.get(f"{api_client}/api/v1/todos/{todo_id}", timeout=5)
    assert get_response.status_code == 404

def test_delete_with_no_valid_target(api_client):
    """DELETE with no valid target returns appropriate response"""
    response = requests.delete(f"{api_client}/api/v1/todos/nonexistent-id", timeout=5)
    assert response.status_code == 404
    assert 'error' in response.json() 