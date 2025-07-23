import pytest
import requests
import time
import os

@pytest.fixture
def api_base_url():
    return os.getenv('API_BASE_URL', 'http://localhost:5000')

@pytest.fixture
def api_client(api_base_url):
    base_url = api_base_url
    # Wait for API to be ready
    max_retries = 30
    for _ in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    
    return base_url 