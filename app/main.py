from flask import Flask, request, jsonify
import uuid
from .todo_service import TodoService

app = Flask(__name__)
todo_service = TodoService()

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/api/v1/todos', methods=['GET'])
def get_todos():
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
        todos = todo_service.search_todos(completed=completed)
    else:
        todos = todo_service.get_all_todos()
    return jsonify(todos)

@app.route('/api/v1/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todo_service.get_todo(todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo)

@app.route('/api/v1/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    todo_data = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': data.get('completed', False)
    }
    
    try:
        todo = todo_service.create_todo(todo_data)
        return jsonify(todo), 201
    except Exception:
        return jsonify({'error': 'Failed to create todo'}), 500

@app.route('/api/v1/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        updated_todo = todo_service.update_todo(todo_id, data)
        if not updated_todo:
            return jsonify({'error': 'Todo not found'}), 404
        return jsonify(updated_todo)
    except Exception:
        return jsonify({'error': 'Failed to update todo'}), 500

@app.route('/api/v1/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        deleted_todo = todo_service.delete_todo(todo_id)
        if not deleted_todo:
            return jsonify({'error': 'Todo not found'}), 404
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception:
        return jsonify({'error': 'Failed to delete todo'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 