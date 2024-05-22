import pytest
from pytest_sqlalchemy_mock.base import *
# from tests.db import Base
from app.app import app
from unittest.mock import MagicMock

# @pytest.fixture(scope="function")
# def sqlalchemy_declarative_base():
    # return Base
# @pytest.fixture
# def endpoint():
#     return "/taxis"

@pytest.fixture
def client():
    client = app.test_client()
    return client

# @pytest.fixture
# def db_session():
#     db = MagicMock()
#     return db
# @pytest.fixture(scope="function")
# def sqlalchemy_mock_config():
#     return [("taxis", [
#      {
#         "id": 7249,
#         "plate": "CNCJ-2997"
#     },
#     {
#         "id": 10133,
#         "plate": "PAOF-6727"
#     },
#     {
#         "id": 2210,
#         "plate": "FGMG-3071"
#     },
#     {
#         "id": 1065,
#         "plate": "GHDN-9291"
#     },
#     {
#         "id": 7956,
#         "plate": "CCKF-1601"
#     }
#     ])]