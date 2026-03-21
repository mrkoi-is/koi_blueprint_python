"""集成测试模板: 演示 Testcontainers 用法

注意: 此测试需要 Docker 环境。在无 Docker 的 CI 环境中会被自动跳过。

使用方式:
    1. 定义 ORM 模型后取消 conftest.py 中 Base.metadata.create_all 的注释
    2. 使用 db_session fixture 获取带事务隔离的数据库 Session
    3. 每个测试用例结束后事务自动回滚，数据不会互相影响
"""
import pytest


# 标记: 需要 Docker 环境的集成测试
pytestmark = pytest.mark.skipif(
    condition=True,  # 改为 False 或移除此标记以启用集成测试
    reason="集成测试模板 — 配置 ORM 模型后启用",
)


def test_db_session_fixture_works(db_session) -> None:
    """验证 db_session fixture 可以正常工作"""
    # db_session 是一个带事务隔离的 SQLAlchemy Session
    # 在此编写使用真实数据库的测试
    assert db_session is not None


def test_crud_example(db_session) -> None:
    """示例: CRUD 集成测试骨架

    步骤:
    1. 创建实体
    2. 查询验证
    3. 更新验证
    4. 删除验证

    注意: 每个测试用例的数据在测试结束后自动回滚
    """
    # from app.domain.example.models import Example
    # entity = Example(name="test")
    # db_session.add(entity)
    # db_session.flush()  # flush 但不 commit，数据在内存中可查
    # assert entity.id is not None
    #
    # found = db_session.get(Example, entity.id)
    # assert found is not None
    # assert found.name == "test"
    pass
