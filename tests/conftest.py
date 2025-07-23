import pytest
import requests
import time
import os

@pytest.fixture
def api_base_url():
    return os.getenv('API_BASE_URL', 'http://localhost:5001')

@pytest.fixture
def api_client(api_base_url):
    base_url = api_base_url
    # Wait for API and AWS services to be ready
    max_retries = 60
    for _ in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                # Additional wait for AWS resources to initialize
                time.sleep(5)
                # Test if AWS services are ready by trying to get todos
                test_response = requests.get(f"{base_url}/api/v1/todos", timeout=5)
                if test_response.status_code == 200:
                    break
        except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
            time.sleep(1)
    
    return base_url 