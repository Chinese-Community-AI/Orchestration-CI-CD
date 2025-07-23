import boto3
import json
import os

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('S3_ENDPOINT', 'http://localhost:4566'),
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        self.bucket_name = 'todo-items'
    
    def _get_object_key(self, todo_id):
        return f'todos/{todo_id}.json'
    
    def create_todo(self, todo):
        key = self._get_object_key(todo['id'])
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(todo),
            ContentType='application/json'
        )
        return todo
    
    def get_todo(self, todo_id):
        try:
            key = self._get_object_key(todo_id)
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return json.loads(response['Body'].read().decode('utf-8'))
        except self.s3_client.exceptions.NoSuchKey:
            return None
    
    def get_all_todos(self):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='todos/'
            )
            todos = []
            for obj in response.get('Contents', []):
                todo_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj['Key'])
                todo = json.loads(todo_response['Body'].read().decode('utf-8'))
                todos.append(todo)
            return todos
        except Exception:
            return []
    
    def update_todo(self, todo):
        return self.create_todo(todo)
    
    def delete_todo(self, todo_id):
        try:
            key = self._get_object_key(todo_id)
            todo = self.get_todo(todo_id)
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return todo
        except Exception:
            return None 