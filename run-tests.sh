#!/bin/bash

echo "Starting TODO API test suite..."

# Start test environment and run tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
TEST_EXIT_CODE=$?

# Clean up
echo "Cleaning up test environment..."
docker-compose -f docker-compose.test.yml down

# Exit with test result status
if [ "$TEST_EXIT_CODE" = "0" ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Tests failed!"
    exit 1
fi 