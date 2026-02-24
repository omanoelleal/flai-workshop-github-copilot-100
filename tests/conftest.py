import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient and restore the in-memory `activities` after each test.

    Arrange: snapshot `app_module.activities`.
    Act: yield a TestClient for tests to use.
    Assert: after the test, restore the original activities state.
    """
    original = copy.deepcopy(app_module.activities)
    client = TestClient(app)
    try:
        yield client
    finally:
        app_module.activities = original
