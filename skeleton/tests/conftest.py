import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from app.core.db import Base
from app.main import app as fastapi_app


@pytest.fixture
def app():
    return fastapi_app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(scope="session")
def postgres_engine():
    """Session 级：整个测试周期只启动一次 PG 容器。"""
    with PostgresContainer("postgres:16-alpine") as container:
        engine = create_engine(container.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine


@pytest.fixture
def db_session(postgres_engine):
    """Function 级：每个测试用例获得独立事务，结束后自动回滚。"""
    connection = postgres_engine.connect()
    transaction = connection.begin()
    session = Session(connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()
