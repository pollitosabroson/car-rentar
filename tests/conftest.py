import tempfile

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function", autouse=True)
def reset_modules():
    """Reset module cache between tests."""
    import sys

    # Remove cached modules
    modules_to_remove = [key for key in sys.modules.keys() if key.startswith("src.")]
    for module in modules_to_remove:
        del sys.modules[module]

    yield


@pytest.fixture(scope="function")
def client(monkeypatch, reset_modules):
    """Create a test client with isolated data directory for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set test data directory
        monkeypatch.setenv("DATA_DIR", tmpdir)

        # Import fresh app
        from src.main import app

        # Create test client
        with TestClient(app) as test_client:
            yield test_client
