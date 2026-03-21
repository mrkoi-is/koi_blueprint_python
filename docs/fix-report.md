# koi_blueprint_python 修复报告

> 生成时间：2026-03-21  
> 目标：针对上一轮深度审计中识别出的高优先级问题逐项修复，并给出当前验证结果与剩余建议。

## 1. 本轮已完成修复

### 1.1 Skeleton 可安装 / 可构建性

- 新增 `skeleton/README.md`，解决 `skeleton/pyproject.toml` 中 `readme = "README.md"` 的悬空问题。
- 新增 `skeleton/.gitignore`，确保 `scripts/apply_skeleton.py` 复制后的新项目具备基础忽略规则。
- 保持 `skeleton/uv.lock` 参与构建，`Dockerfile` 继续兼容“有锁 / 无锁”两种初始化场景。

### 1.2 数据库生命周期与依赖注入

- 新增 `skeleton/app/core/db.py`，提供共享 `Base`，作为 ORM 与 Alembic 的统一 metadata 来源。
- 重构 `skeleton/app/core/dependencies.py`：
  - 新增 `init_database()` / `shutdown_database()`
  - 新增 `get_session_factory()`
  - `get_db_session()` / `get_uow()` 改为从 `app.state` 获取 session factory
- 更新 `skeleton/app/main.py`：在 Lifespan 中初始化并释放数据库资源，消除导入期全局 engine 初始化。

### 1.3 Alembic 接线

- 更新 `skeleton/migrations/env.py`：
  - 通过 `settings.database_url` 覆盖 `sqlalchemy.url`
  - 使用 `app.core.db.Base.metadata` 作为 `target_metadata`
- 结果：迁移模板不再停留在 `target_metadata = None` 的不可用状态。

### 1.4 认证基线一致性

- 更新 `skeleton/app/core/auth.py`：
  - `HTTPBearer(auto_error=False)`
  - 缺失凭证时统一抛出 `AuthenticationError()`
- 新增对应单测覆盖，确保“无 Token”返回 401 语义而不是框架默认 403。

### 1.5 响应契约统一

- 更新 `skeleton/app/core/responses.py`：`ApiResponse.code` 从 `int` 统一为 `str`，默认值为 `"OK"`。
- 同步更新 `docs/architecture.md` 中相关代码片段，避免成功 / 失败响应在 `code` 字段上类型不一致。

### 1.6 测试模板可执行性

- 更新 `skeleton/tests/conftest.py`：使用 `Base.metadata.create_all(engine)`。
- 更新 `skeleton/tests/integration/test_example_crud.py`：
  - 由永久 `condition=True` 跳过改为动态检测 Docker 可用性
  - 使用 `SELECT 1` / `SELECT current_database()` 做真实连通性验证
- 保留 `integration` marker，避免模板误导。

### 1.7 Skill 与脚本路径冲突

- 旧问题：Skill 文档中的 `scripts/...` 会优先命中 `.agent/skills/*/scripts/` 下的陈旧脚本。
- 本轮修复：
  - 将 `.agent/skills/server-init/scripts/apply_skeleton.py`
  - `.agent/skills/add-domain-module/scripts/scaffold_domain.py`
  - `.agent/skills/add-infra-adapter/scripts/scaffold_adapter.py`
  全部改为委托执行仓库根级 `scripts/` 实现。
- 结果：Skill 实际执行路径与仓库维护入口统一，不再出现“文档已修，Skill 仍调用旧逻辑”的分叉。

### 1.8 根级脚手架质量

- 重写 `scripts/scaffold_domain.py`：
  - 使用共享 `app.core.db.Base`
  - 生成可工作的 Repository / UoW / Service / Router
  - 自动更新 `app/main.py` 注册路由
  - 测试输出统一到 `tests/unit/test_<module>_service.py`
  - 生成可运行的 MemoryRepository 单测，而不是占位 `assert True`
- 重写 `scripts/scaffold_adapter.py`：
  - 生成 `app/infra/<adapter>/__init__.py`
  - 生成 `abstract.py` / `<impl>.py` / `memory.py`
  - 与 Skill reference 中的 adapter pattern 对齐

### 1.9 文档与示例措辞

- 更新 `README.md`：
  - `examples/minimal-service/` 改为“最小结构样例”
  - `examples/device/` 改为“完整领域分层示例（需在项目中接线 DI）”
- 更新 `examples/minimal-service/README.md`：明确其为示例代码片段，不是独立打包单元。
- 更新 `.agent/skills/add-domain-module/references/domain-patterns.md`：测试路径改为 `tests/unit/test_<module>_service.py`。
- 更新 `docs/architecture.md`：同步 `db.py`、认证依赖、ApiResponse、Alembic 接线与依赖注入示例。

## 2. 本轮验证结果

### 2.1 已完成验证

- `python3 -m compileall -q skeleton/app skeleton/tests examples scripts .agent/skills` ✅
- `python3 scripts/apply_skeleton.py --help` ✅
- `python3 scripts/scaffold_domain.py --help` ✅
- `python3 scripts/scaffold_adapter.py --help` ✅
- 在临时虚拟环境中执行 `ruff check skeleton scripts .agent/skills` ✅
- 在临时虚拟环境中执行 `pytest tests/unit tests/test_health.py -q` ✅（21 项通过）

### 2.2 环境说明

- 宿主环境仍缺少 `uv`，因此未直接使用 `uv sync` / `uv run ...`。
- 本轮验证通过临时虚拟环境补装依赖后完成。
- `pyright` 在当前临时 `pip` 环境中无法直接安装，因此**未完成本地类型检查**；后续仍建议在标准 `uv` 环境或 CI 中执行 `uv run pyright`。

## 3. 修复后仍建议持续优化的点

以下不再属于阻塞项，但仍建议后续继续完善：

1. 为 `skeleton` 增加一个真实可迁移的领域模块示例，以便 Alembic / API / 集成测试形成完整闭环。
2. 将 `examples/device/` 进一步升级为真正可运行的端到端示例，而不仅是“需接线 DI”的分层参考。
3. 为新增加的 Skill（如 `add-background-task`、`add-websocket`、`add-observability`）补充脚本或模板资产，而不仅是工作流说明。
4. 在具备 `uv` 的环境下执行一次完整门禁：`ruff + pyright + pytest + docker build`。

## 4. 关键修复文件

- `skeleton/app/core/db.py`
- `skeleton/app/core/dependencies.py`
- `skeleton/app/main.py`
- `skeleton/app/core/auth.py`
- `skeleton/app/core/responses.py`
- `skeleton/migrations/env.py`
- `skeleton/tests/conftest.py`
- `skeleton/tests/integration/test_example_crud.py`
- `scripts/scaffold_domain.py`
- `scripts/scaffold_adapter.py`
- `.agent/skills/server-init/scripts/apply_skeleton.py`
- `.agent/skills/add-domain-module/scripts/scaffold_domain.py`
- `.agent/skills/add-infra-adapter/scripts/scaffold_adapter.py`
- `docs/architecture.md`

## 5. 总结

本轮修复后，`koi_blueprint_python` 已从“文档领先、实现分叉”明显提升为“骨架、迁移、脚手架、Skill 路径基本一致”的状态。

当前最重要的高优先级问题已完成收敛：

- 骨架 readme 缺失
- `.gitignore` 未随 skeleton 分发
- 导入期数据库初始化
- Alembic metadata 未接线
- 鉴权 401/403 语义不一致
- Skill 指向旧脚本
- 领域/适配器脚手架输出质量偏低
- 集成测试永久跳过

