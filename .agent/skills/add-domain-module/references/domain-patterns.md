# Domain Module Pattern

## 1. 标准文件结构

一个标准领域模块通常包含：
- `router.py`
- `schemas.py`
- `models.py`
- `service.py`
- `repository.py`
- `repository_sa.py`
- `uow.py`
- `tests/unit/test_<module>_service.py`

## 2. 分层职责

- `router.py`：HTTP 入参、状态码、响应 DTO、依赖注入
- `schemas.py`：Pydantic DTO / API 契约
- `models.py`：ORM 模型
- `service.py`：业务规则与用例编排
- `repository.py`：仓储抽象接口
- `repository_sa.py`：SQLAlchemy 实现
- `uow.py`：事务边界与仓储聚合

## 3. 注册与接线

- 新增 router 后，要在 `app/main.py` 或统一入口中注册
- 模型变更后，要补 Alembic migration
- 依赖注入应通过 `app/core/dependencies.py` 或 composition root 完成

## 4. 测试建议

- service 行为优先放在 `tests/unit/`
- API / DB 接线优先放在 `tests/integration/`
- 不要保留永久占位 `assert True`

## 5. 设计约束

- router 只保留 HTTP 关注点
- service 不直接依赖 FastAPI
- repository 隔离持久化细节
- 命名应贴近业务领域，而不是技术实现
