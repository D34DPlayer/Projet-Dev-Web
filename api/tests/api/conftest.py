import pytest
from fastapi.testclient import TestClient
from datetime import timedelta

from api.main import app
from api.app import create_access_token


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def token():
    return "Bearer " + create_access_token(data={"sub": "admin"}, expires_delta=timedelta(minutes=5))


@pytest.fixture(scope="session")
def headers(token):
    return dict(Authorization=token)
