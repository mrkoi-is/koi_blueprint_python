from collections.abc import Generator

from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.core.uow import SqlAlchemyUnitOfWork


def init_database(app: FastAPI) -> None:
    engine = create_engine(settings.database_url)
    app.state.db_engine = engine
    app.state.session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )


def shutdown_database(app: FastAPI) -> None:
    engine: Engine | None = getattr(app.state, "db_engine", None)
    if engine is not None:
        engine.dispose()


def get_session_factory(request: Request) -> sessionmaker[Session]:
    session_factory: sessionmaker[Session] | None = getattr(
        request.app.state, "session_factory", None
    )
    if session_factory is None:
        raise RuntimeError("Database session factory has not been initialized")
    return session_factory


def get_db_session(request: Request) -> Generator[Session]:
    session_factory = get_session_factory(request)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def get_uow(request: Request) -> SqlAlchemyUnitOfWork:
    session_factory = get_session_factory(request)
    return SqlAlchemyUnitOfWork(session_factory)
