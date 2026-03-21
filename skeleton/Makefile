.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-12s %s\n", $$1, $$2}'

dev: ## 启动开发服务器
	uv run uvicorn app.main:app --reload

lint: ## 运行 Ruff 检查
	uv run ruff check .

format: ## 运行 Ruff 格式化
	uv run ruff format .

typecheck: ## 运行 pyright
	uv run pyright

test: ## 运行 pytest
	uv run pytest
