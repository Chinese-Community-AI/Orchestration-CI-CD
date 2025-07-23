import boto3
import os
from datetime import datetime

class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:4566'),
            region_name='us-east-1',
            aws_access_key_id='test',
            aws_secret_access_key='test'
        )
        self.table_name = 'todos'
        self.table = self.dynamodb.Table(self.table_name)
    
    def create_todo(self, todo):
        todo['created_date'] = datetime.utcnow().isoformat()
        todo['updated_date'] = datetime.utcnow().isoformat()
        self.table.put_item(Item=todo)
        return todo
    
    def get_todo(self, todo_id):
        response = self.table.get_item(Key={'id': todo_id})
        return response.get('Item')
    
    def get_all_todos(self):
        response = self.table.scan()
        return response.get('Items', [])
    
    def update_todo(self, todo_id, updates):
        updates['updated_date'] = datetime.utcnow().isoformat()
        
        update_expression = 'SET '
        expression_values = {}
        
        for key, value in updates.items():
            update_expression += f'{key} = :{key}, '
            expression_values[f':{key}'] = value
        
        update_expression = update_expression.rstrip(', ')
        
        response = self.table.update_item(
            Key={'id': todo_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues='ALL_NEW'
        )
        return response.get('Attributes')
    
    def delete_todo(self, todo_id):
        response = self.table.delete_item(
            Key={'id': todo_id},
            ReturnValues='ALL_OLD'
        )
        return response.get('Attributes') 