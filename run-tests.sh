#!/bin/bash

echo "Starting TODO API test suite..."

# Start test environment and run tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Get exit code from test runner
EXIT_CODE=$(docker-compose -f docker-compose.test.yml ps -q test-runner | xargs docker inspect --format='{{.State.ExitCode}}')

# Clean up
echo "Cleaning up test environment..."
docker-compose -f docker-compose.test.yml down

# Exit with test result status
if [ "$EXIT_CODE" = "0" ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi 