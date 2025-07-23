# TODO REST API with Cloud Orchestration

A REST API for managing TODO items with DynamoDB and S3 storage using LocalStack for local development.

## Requirements

- Docker and Docker Compose
- Git

## Running the Application

Start the development environment:

```bash
./run-stack.sh
```

This starts LocalStack (with DynamoDB and S3) and the API server. The API will be available at http://localhost:5001.

To stop the application, press Ctrl+C.

## Running Tests

Execute the test suite:

```bash
./run-tests.sh
```

This runs all tests in an isolated environment and cleans up afterwards. Tests will pass with exit code 0 or fail with exit code 1.

## API Endpoints

### Health Check

- GET `/health` - Returns server status

### TODO Operations

- GET `/api/v1/todos` - List all todos
- GET `/api/v1/todos?completed=true` - Filter by completion status
- GET `/api/v1/todos/{id}` - Get specific todo
- POST `/api/v1/todos` - Create new todo
- PUT `/api/v1/todos/{id}` - Update existing todo
- DELETE `/api/v1/todos/{id}` - Delete todo

### Example Usage

Create a todo:

```bash
curl -X POST http://localhost:5001/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and bread"}'
```

List all todos:

```bash
curl http://localhost:5001/api/v1/todos
```

## Data Storage

Each TODO item is stored in both:

- DynamoDB table (primary storage)
- S3 bucket as JSON object (backup storage)

LocalStack provides local versions of these AWS services for development and testing.

## CI/CD

GitHub Actions automatically runs tests on:

- Push to main branch
- Pull requests to main branch
- Manual workflow triggers

## Project Structure

- `app/` - Flask application code
- `tests/` - Test suite
- `docker-compose.yml` - Development environment
- `docker-compose.test.yml` - Testing environment
- `run-stack.sh` - Start development stack
- `run-tests.sh` - Execute test suite
