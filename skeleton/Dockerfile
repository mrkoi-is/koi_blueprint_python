# ---- Stage 1: Build ----
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 两种模式:
# 1. 有 uv.lock (推荐): COPY pyproject.toml uv.lock → uv sync --frozen
# 2. 无 uv.lock (初始化): COPY pyproject.toml → uv sync (自动生成 lock)
COPY pyproject.toml uv.lock* ./
RUN if [ -f uv.lock ]; then \
      uv sync --frozen --no-dev --no-install-project; \
    else \
      uv sync --no-dev --no-install-project; \
    fi

COPY . .
RUN if [ -f uv.lock ]; then \
      uv sync --frozen --no-dev; \
    else \
      uv sync --no-dev; \
    fi

# ---- Stage 2: Runtime ----
FROM python:3.13-slim AS runtime

WORKDIR /app
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
