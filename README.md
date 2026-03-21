# koi_blueprint_python

面向 AI Agent 的 Python 服务端架构蓝图仓库。

这个仓库的目标是让 AI 用统一方式生成符合 Koi 标准的 Python 服务端项目。它同时提供：

- `docs/architecture.md`：通用架构规范（1000+ 行，覆盖工具链 → 架构模式 → 约束清单 → 可观测性 → API 版本管理）
- `skeleton/`：可直接复制的最小可运行骨架（含完整 core 模块、测试、CI、Docker）
- `examples/`：最小服务、领域模块、异步服务示例
- `.agent/skills/`：9 个可安装的 AI Agent Skill

## 使用方式

### 模式一：知识库模式

让 AI 直接阅读：

1. `README.md`
2. `docs/architecture.md`
3. `skeleton/`
4. `examples/`

适合不能自动发现 Skill 的环境。

### 模式二：已安装 Skill 模式

将 `.agent/skills/*` 安装或软链接到 Agent 可发现的位置后，直接触发对应 Skill：

- Codex 类环境：安装或软链接到 `$CODEX_HOME/skills/`
- Cursor：同步到 `.cursor/skills/`

## 目录导航

- `docs/architecture.md`：Koi Python 服务端通用架构标准 (v4.0)
- `skeleton/`：最小可运行项目骨架
- `examples/minimal-service/`：最小可运行金样例
- `examples/device/`：完整领域模块示例
- `examples/async-service/`：完整异步路径示例
- `.agent/skills/`：9 个 Skill 源码目录
- `scripts/`：根级脚手架脚本

## 技术栈

- Python 3.12+ (新项目推荐 3.13)
- FastAPI + Pydantic v2
- SQLAlchemy 2.0 (Mapped)
- uv + Ruff + pyright (Astral 工具链)
- structlog + Prometheus (可观测性)
- Testcontainers + pytest
- Bandit + pip-audit (安全扫描)

## Skill 列表

| Skill | 用途 |
|---|---|
| `server-init` | 从 skeleton 初始化新项目 |
| `add-domain-module` | 脚手架领域模块 |
| `add-infra-adapter` | 脚手架基础设施适配器 |
| `alembic-migration` | 数据库迁移管理 |
| `ci-setup` | CI/CD 流水线配置 |
| `docker-deploy` | Docker 部署资产准备 |
| `add-background-task` | 后台任务集成 (Celery/ARQ) |
| `add-websocket` | WebSocket 支持 |
| `add-observability` | Prometheus + OpenTelemetry |

## 开发建议

1. 先维护 `docs/architecture.md`
2. 再维护 `skeleton/`，确保 `pytest` 可通过
3. 再补充 `examples/`
4. 最后完善 `.agent/skills/` 中的脚本、模板与 references
