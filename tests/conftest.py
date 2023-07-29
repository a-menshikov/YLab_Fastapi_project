from app.main import app
from fastapi.testclient import TestClient

pytest_plugins = "tests.fixtures"

client = TestClient(app)
