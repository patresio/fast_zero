import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.app import database as app_database


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db_before_each_test():
    """Fixture to clear the in-memory database before each test."""
    app_database.clear()
