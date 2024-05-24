"""Module to define fixtures for pytest tests.
"""
import pytest
from app.app import app

@pytest.fixture
def client():
    """Fixture for creating a test client for the Flask application.

    Returns:
        FlaskClient: A test client for making requests to the Flask application.
    """
    client = app.test_client()
    return client

