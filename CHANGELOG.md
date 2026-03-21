# Changelog

本项目的所有重要变更记录在此文件中。
格式基于 [Keep a Changelog](https://keepachangelog.com/)。

## [Unreleased]

### Added
- `app/core/repository.py` — Generic CRUD Repository 基类 (AbstractRepository + SaRepository + MemoryRepository)
- `app/core/metrics.py` — Prometheus 指标收集模板
- `.pre-commit-config.yaml` — Ruff pre-commit hooks
- `docker-compose.yml` — 本地开发 PostgreSQL + Redis 编排
- `.dockerignore` — Docker 构建上下文排除
- `tests/unit/test_exceptions.py` — 异常体系示范测试
- `tests/unit/test_auth.py` — 认证依赖示范测试
- `tests/integration/test_example_crud.py` — Testcontainers 集成测试模板
- `examples/async-service/` — 完整异步路径示例 (AsyncSession, async UoW, async Repository)
- `.agent/skills/add-background-task/` — 后台任务 Skill
- `.agent/skills/add-websocket/` — WebSocket Skill
- `.agent/skills/add-observability/` — 可观测性 Skill
- `scripts/apply_skeleton.py` — 项目根级 skeleton 应用脚本
- `scripts/scaffold_domain.py` — 项目根级领域模块脚手架
- `scripts/scaffold_adapter.py` — 项目根级基础设施适配器脚手架
- `CONTRIBUTING.md` — 贡献指南
- `.editorconfig` — 编辑器统一配置
- Architecture doc §9 可观测性 (Prometheus, OpenTelemetry)
- Architecture doc §10 速率限制 (slowapi)
- Architecture doc §11 API 版本管理

### Changed
- `app/core/logging.py` — 添加标准库 logging 桥接，uvicorn/sqlalchemy 日志格式统一
- `app/main.py` — `setup_logging()` 移至 `create_app()` 而非 lifespan
- `Dockerfile` — Python 3.13-slim + uv.lock + --frozen 确定性构建
- `pyproject.toml` — target-version py313, 添加 bandit/pip-audit/pytest-cov, ruff S 规则
- `Makefile` — 新增 test-unit, test-cov, migrate, security, up, down 命令
- `tests/conftest.py` — 添加 db_session fixture with join_transaction_mode
- `.github/workflows/ci.yml` — Python 3.13, 添加 coverage/bandit/pip-audit steps

### Fixed
- Architecture doc 与 skeleton 代码之间 6 处漂移已全部消除

## [0.1.0] - 2026-03-21

### Added
- 初始版本：architecture.md, skeleton, examples, 6 agent skills
