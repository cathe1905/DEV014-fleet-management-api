import pytest
from app.app import app

@pytest.fixture
def endpoint():
    return "/taxis"

@pytest.fixture
def client():
    client = app.test_client()
    return client

