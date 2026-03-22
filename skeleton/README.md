# Koi Skeleton

Koi Python 服务骨架 — 最小可运行的 FastAPI 项目模板。  
Koi Python service skeleton — minimal runnable FastAPI project template.

## Quick Start / 快速开始

```bash
# 1. Install dependencies / 安装依赖
uv sync --all-groups

# 2. Copy environment config / 复制环境配置
cp .env.example .env

# 3. Run tests / 运行测试
uv run pytest

# 4. Start dev server / 启动开发服务器
uv run uvicorn app.main:app --reload
```

## Environment Variables / 环境变量

| Variable | Default | Description |
|---|---|---|
| `APP_APP_NAME` | `Koi Service` | 应用名称 / Application name |
| `APP_DEBUG` | `false` | 调试模式 / Debug mode |
| `APP_DATABASE_URL` | `postgresql+psycopg://...` | 数据库连接 / Database connection URL |
| `APP_JWT_SECRET` | *(required)* | JWT 签名密钥 / JWT signing secret |
| `APP_REDIS_URL` | `redis://localhost:6379/0` | Redis 连接 / Redis connection URL |
| `APP_CORS_ORIGINS` | `["http://localhost:3000"]` | CORS 允许来源 / CORS allowed origins |

> See `.env.example` for a complete template. / 完整模板见 `.env.example`。

## Make Commands / 开发命令

| Command | Description |
|---|---|
| `make dev` | Start dev server / 启动开发服务器 |
| `make lint` | Run Ruff linter / 运行 Ruff 检查 |
| `make format` | Format code / 格式化代码 |
| `make typecheck` | Run Pyright / 运行 Pyright 类型检查 |
| `make test` | Run all tests / 运行全部测试 |
| `make test-unit` | Run unit tests only / 仅运行单元测试 |
| `make test-cov` | Run tests with coverage / 运行测试并输出覆盖率 |
| `make security` | Run Bandit + pip-audit / 安全扫描 |
| `make migrate` | Run Alembic migrations / 运行数据库迁移 |
| `make up` | Start docker-compose services / 启动 Docker 依赖 |
| `make down` | Stop docker-compose services / 停止 Docker 依赖 |

## Project Structure / 项目结构

```
app/
├── __init__.py
├── config.py           # pydantic-settings 配置 / Settings
├── main.py             # create_app() 工厂函数 / App factory
├── core/
│   ├── auth.py         # JWT 认证依赖 / JWT auth dependencies
│   ├── db.py           # SQLAlchemy Base / DB base model
│   ├── dependencies.py # 生命周期管理 / Lifecycle dependencies
│   ├── exceptions.py   # 统一异常体系 / Unified exception hierarchy
│   ├── exception_handlers.py # 异常处理器 / Exception handlers
│   ├── logging.py      # structlog 初始化 / Structured logging
│   ├── metrics.py      # Prometheus 指标 / Prometheus metrics
│   ├── pagination.py   # 分页参数 / Pagination params
│   ├── repository.py   # 泛型仓储基类 / Generic repository
│   ├── responses.py    # 统一响应格式 / Unified response format
│   └── uow.py          # 工作单元 / Unit of Work
├── domain/             # 领域模块 / Domain modules
└── infra/              # 基础设施适配器 / Infra adapters
tests/
├── conftest.py         # 通用 fixture / Shared fixtures
├── test_health.py      # 健康检查测试 / Health check test
├── unit/               # 单元测试 / Unit tests
├── integration/        # 集成测试 (需要 Docker) / Integration tests (need Docker)
└── domain/             # 领域测试 / Domain tests
```

## Docker / 容器化

```bash
# Start local PostgreSQL + Redis / 启动本地 PG + Redis
make up

# Build Docker image / 构建镜像
docker build -t koi-service .
```

## Notes / 说明

- `migrations/env.py` 已接入 `app.core.db.Base.metadata`
- 集成测试使用 Testcontainers 自动管理 PostgreSQL 容器
- `app/core/metrics.py` 提供 Prometheus 指标（需安装 `prometheus-fastapi-instrumentator`）
