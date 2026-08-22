import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.mktemp(suffix='.db')}"
os.environ["AI_API_KEY"] = ""  # force demo mode in tests, deterministic and free

from fastapi.testclient import TestClient  # noqa: E402
from backend.main import app  # noqa: E402
from backend.database.database import Base, engine  # noqa: E402
import backend.models  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


def register_and_login(client, role="student", email=None):
    email = email or f"{role}_{os.urandom(4).hex()}@example.com"
    payload = {
        "name": f"Test {role.title()}",
        "email": email,
        "password": "password123",
        "role": role,
    }
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 200, resp.text
    return resp.json()
