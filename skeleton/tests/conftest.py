import os
from collections.abc import Generator

# 测试环境默认启用 debug 模式，避免 JWT 弱密钥检查阻断测试
# Default to debug mode in tests to prevent JWT secret validator from blocking
os.environ.setdefault("APP_DEBUG", "true")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]

from app.core.db import Base
from app.main import app as fastapi_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(fastapi_app)


@pytest.fixture(scope="session")
def postgres_engine() -> Generator[Engine]:
    """Session 级：整个测试周期只启动一次 PG 容器。"""
    with PostgresContainer("postgres:16-alpine", driver="psycopg") as container:
        engine = create_engine(container.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine


@pytest.fixture
def db_session(postgres_engine: Engine) -> Generator[Session]:
    """Function 级：每个测试用例获得独立事务，结束后自动回滚。"""
    connection = postgres_engine.connect()
    transaction = connection.begin()
    session = Session(connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()
