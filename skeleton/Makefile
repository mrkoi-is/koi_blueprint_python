.DEFAULT_GOAL := help

help:       ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-12s %s\n", $$1, $$2}'

dev:        ## 启动开发服务器
	uv run uvicorn app.main:app --reload

lint:       ## 运行 Ruff 检查并自动修复
	uv run ruff check . --fix

format:     ## 运行 Ruff 格式化
	uv run ruff format .

typecheck:  ## 运行 pyright 类型检查
	uv run pyright

test:       ## 运行全部测试
	uv run pytest

test-unit:  ## 仅运行单元测试
	uv run pytest tests/unit

test-cov:   ## 运行测试并生成覆盖率报告
	uv run pytest --cov=app --cov-report=html --cov-report=term-missing

migrate:    ## 执行数据库迁移
	uv run alembic upgrade head

security:   ## 安全扫描 (Bandit + pip-audit)
	uv run bandit -r app/ -q
	uv run pip-audit

up:         ## 启动本地基础设施 (PostgreSQL + Redis)
	docker compose up -d

down:       ## 停止本地基础设施
	docker compose down
