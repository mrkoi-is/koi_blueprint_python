"""集成测试模板: 演示 Testcontainers 用法。"""

import shutil
import subprocess

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session


def _docker_available() -> bool:
    docker = shutil.which("docker")
    if docker is None:
        return False
    result = subprocess.run(
        [docker, "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _docker_available(), reason="Docker 不可用，跳过集成测试"),
]


def test_db_session_fixture_works(db_session: Session) -> None:
    result = db_session.execute(text("SELECT 1")).scalar_one()
    assert result == 1


def test_db_connection_exposes_database_name(db_session: Session) -> None:
    result = db_session.execute(text("SELECT current_database()")).scalar_one()
    assert isinstance(result, str)
