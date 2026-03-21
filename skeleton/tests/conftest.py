import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
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
    """Session 级：整个测试周期只启动一次 PG 容器"""
    with PostgresContainer("postgres:16-alpine") as container:
        engine = create_engine(container.get_connection_url())
        # Base.metadata.create_all(engine)  # 项目有 ORM 模型后取消注释
        yield engine
    # 测试结束，容器自动销毁


@pytest.fixture
def db_session(postgres_engine):
    """Function 级：每个测试用例获得独立的事务，测试结束自动回滚

    SQLAlchemy 2.0 写法：
      - Session(connection, join_transaction_mode="create_savepoint")
      - join_transaction_mode 确保 session 加入外部事务而非自动提交
    """
    connection = postgres_engine.connect()
    transaction = connection.begin()
    session = Session(connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()
