#!/bin/bash

echo "Initializing AWS resources..."

# Create DynamoDB table
aws dynamodb create-table \
    --table-name todos \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --endpoint-url=http://localhost:4566 \
    --region us-east-1

# Create S3 bucket
aws s3 mb s3://todo-items \
    --endpoint-url=http://localhost:4566 \
    --region us-east-1

echo "AWS resources initialized successfully!" 