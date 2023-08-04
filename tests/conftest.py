from fastapi.testclient import TestClient

from app.main import app

pytest_plugins = 'tests.fixtures'

client = TestClient(app)
