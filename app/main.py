from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/api/v1/todos', methods=['GET'])
def get_todos():
    return jsonify([])

@app.route('/api/v1/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/v1/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    todo = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False
    }
    return jsonify(todo), 201

@app.route('/api/v1/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/v1/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 