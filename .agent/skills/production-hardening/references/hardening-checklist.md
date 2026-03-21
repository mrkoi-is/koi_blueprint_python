# Hardening Checklist

## 1. Runtime Safety

- `.env.example` 明确标注示例值不可用于生产
- JWT secret / DB URL / CORS 等默认值是否安全
- `/health` 是否存在
- 是否需要 `/ready` 或更细粒度探针

## 2. Build Reproducibility

- 是否存在 `uv.lock`
- `Dockerfile` 是否使用确定性安装
- `.dockerignore` 是否排除无关上下文
- 是否避免静默忽略安装失败

## 3. CI Quality Gates

- `ruff`
- `pytest`
- `pyright`
- coverage
- security scan (`bandit`, `pip-audit`)
- Docker build smoke check

## 4. Observability

- structlog 初始化是否统一
- stdlib logging 是否桥接
- metrics 是否可启用
- 错误响应 / trace_id 是否清晰

## 5. Deploy Readiness

- `docker-compose.yml` 是否提供本地依赖
- 镜像是否暴露健康检查
- 是否存在清晰的上线前检查项
