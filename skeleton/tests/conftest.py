import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

from app.main import app as fastapi_app


@pytest.fixture
def app():
    return fastapi_app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(scope="session")
def postgres_engine():
    with PostgresContainer("postgres:16-alpine") as container:
        engine = create_engine(container.get_connection_url())
        yield engine
