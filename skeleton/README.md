# Koi Skeleton

Koi Python 服务骨架。

## 用途

- 作为新项目初始化后的项目根目录内容
- 提供最小可运行的 `FastAPI + SQLAlchemy + Alembic + pytest` 结构
- 作为 `scripts/apply_skeleton.py` 的复制源

## 快速开始

```bash
uv sync --all-groups
cp .env.example .env
uv run pytest
uv run uvicorn app.main:app --reload
```

## 开发命令

```bash
make dev
make lint
make format
make typecheck
make test
make test-cov
make security
```

## 说明

- `tests/unit/`：单元测试
- `tests/integration/`：集成测试模板（需要 Docker）
- `docker-compose.yml`：本地 PostgreSQL + Redis
- `migrations/env.py`：已接入 `app.core.db.Base.metadata`
