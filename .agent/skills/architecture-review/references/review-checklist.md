# Architecture Review Checklist

## 1. 入口与生命周期

- `app/main.py` 是否使用 `create_app()`
- 日志是否在应用创建早期初始化
- 数据库/Redis 等资源是否由 Lifespan 管理
- 是否避免导入期创建全局连接

## 2. 配置与核心基建

- `app/config.py` 是否使用 `pydantic-settings`
- `app/core/db.py` 是否存在共享 `Base`
- `migrations/env.py` 是否接入 `Base.metadata`
- `app/core/exceptions.py` / `exception_handlers.py` 是否统一
- `app/core/logging.py` 是否统一 structlog 与 stdlib logging

## 3. 认证与权限

- 是否存在 `get_current_user` / `get_optional_user`
- 缺失凭证是否返回一致的 401 语义
- 角色校验是否通过依赖工厂封装
- 是否有最基础 auth 单测

## 4. 领域分层

- `router.py` 只做 HTTP concerns
- `service.py` 保持纯业务逻辑
- `repository.py` / `repository_sa.py` 职责是否分离
- `uow.py` 是否挂载领域仓储
- 是否存在对框架/ORM 的反向泄漏

## 5. 测试与质量

- `tests/unit/` / `tests/integration/` 是否分层
- 是否有 `conftest.py` 管理通用 fixture
- Testcontainers 是否可启用而不是永久跳过
- `ruff` / `pytest` / `pyright` / coverage 是否在 CI 中执行

## 6. 交付与运维

- `Dockerfile` 是否支持确定性构建
- `.dockerignore` / `.gitignore` 是否齐全
- `docker-compose.yml` 是否提供最小本地依赖
- 是否有安全扫描与可观测性入口

## 7. 产出格式建议

- 总评
- 亮点
- 差距
- `P0 / P1 / P2` 改进建议
- 关键文件路径
