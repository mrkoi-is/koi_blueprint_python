# Testing Patterns

## 1. 目录标准

- `tests/unit/`：Service、Core、MemoryRepository、fake UoW
- `tests/integration/`：真实数据库、Testcontainers、API/事务行为
- `tests/conftest.py`：共享 fixture

## 2. Unit Test 模式

适用场景：
- `service.py`
- `auth.py`
- `exceptions.py`
- `repository.py` 中的 memory doubles

推荐模式：
- fake UoW
- MemoryRepository
- 明确断言行为、状态与异常

## 3. Integration Test 模式

适用场景：
- 数据库连接
- 事务回滚
- FastAPI route + dependency wiring
- Alembic / metadata / create_all 最小闭环

推荐模式：
- 动态检测 Docker 可用性
- `pytest.mark.integration`
- 不要永久 `condition=True`

## 4. 质量门禁

- `pytest`
- `pytest-cov`
- `ruff`
- `pyright`

## 5. 反模式

- `assert True`
- 永久 skip 的模板测试
- 在 unit tests 中依赖真实数据库
- 在 integration tests 中重复造大量业务数据装配逻辑
