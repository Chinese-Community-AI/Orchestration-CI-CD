from .dynamodb_service import DynamoDBService
from .s3_service import S3Service

class TodoService:
    def __init__(self):
        self.dynamodb_service = DynamoDBService()
        self.s3_service = S3Service()
    
    def create_todo(self, todo_data):
        try:
            todo = self.dynamodb_service.create_todo(todo_data)
            self.s3_service.create_todo(todo)
            return todo
        except Exception as e:
            # If DynamoDB succeeded but S3 failed, try to clean up DynamoDB
            if 'id' in todo_data:
                try:
                    self.dynamodb_service.delete_todo(todo_data['id'])
                except Exception:
                    pass
            raise e
    
    def get_todo(self, todo_id):
        return self.dynamodb_service.get_todo(todo_id)
    
    def get_all_todos(self):
        return self.dynamodb_service.get_all_todos()
    
    def update_todo(self, todo_id, updates):
        try:
            existing_todo = self.dynamodb_service.get_todo(todo_id)
            if not existing_todo:
                return None
            
            updated_todo = self.dynamodb_service.update_todo(todo_id, updates)
            if updated_todo:
                self.s3_service.update_todo(updated_todo)
            return updated_todo
        except Exception as e:
            raise e
    
    def delete_todo(self, todo_id):
        try:
            deleted_todo = self.dynamodb_service.delete_todo(todo_id)
            if deleted_todo:
                self.s3_service.delete_todo(todo_id)
            return deleted_todo
        except Exception as e:
            raise e
    
    def search_todos(self, completed=None):
        todos = self.get_all_todos()
        if completed is not None:
            todos = [todo for todo in todos if todo.get('completed') == completed]
        return todos 