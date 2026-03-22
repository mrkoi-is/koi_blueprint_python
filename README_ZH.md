# koi_blueprint_python

[![CI](https://github.com/mrkoi-is/koi_blueprint_python/actions/workflows/ci.yml/badge.svg)](https://github.com/mrkoi-is/koi_blueprint_python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mrkoi-is/koi_blueprint_python/graph/badge.svg)](https://codecov.io/gh/mrkoi-is/koi_blueprint_python)
![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue)
[![License: MIT](https://img.shields.io/github/license/mrkoi-is/koi_blueprint_python)](LICENSE)

[English](README.md)

面向 AI Agent 的 Python 服务端架构蓝图仓库。

---

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/mrkoi-is/koi_blueprint_python.git
cd koi_blueprint_python/skeleton

# 2. 安装依赖
uv sync --all-groups

# 3. 检查 + 类型检查 + 测试
uv run ruff check .
uv run pyright
uv run pytest
```

> 详见 `docs/ai-quickstart.md` 获取 AI 最短上手路径。

---

## 仓库内容

这个仓库的目标是让 AI 用统一方式生成符合 Koi 标准的 Python 服务端项目。它同时提供：

- `docs/architecture.md` — 通用架构规范（1000+ 行，覆盖工具链 → 架构模式 → 约束清单 → 可观测性 → API 版本管理）
- `skeleton/` — 可直接复制的最小可运行骨架（含完整 core 模块、测试、CI、Docker）
- `examples/` — 最小服务、领域模块、异步服务示例
- `.agent/skills/` — 16 个可安装的 AI Agent Skill（与本仓库同发，当前统一按 `docs/architecture.md` v4.0 维护）

## 使用方式

### 模式一：知识库模式

让 AI 直接阅读：

1. `docs/ai-quickstart.md`
2. `README.md`
3. `docs/architecture.md`
4. `skeleton/`
5. `examples/`

适合不能自动发现 Skill 的环境。

### 模式二：工具原生发现（推荐）

| 工具 | 发现方式 |
|------|---------|
| **Google Antigravity** | 工作区级 Skill 官方路径即为 `.agent/skills/`，与本仓库一致；`SKILL.md` 的 `description` 供 Agent 路由索引。 |
| **OpenAI Codex（CLI/IDE）** | 仓库根目录 `AGENTS.md` 说明 Skill 索引与必读文档；可选将 `.agent/skills/*` 软链到 `$CODEX_HOME/skills/` 供全局 Codex 使用。 |
| **Cursor** | `.cursor/rules/koi-agent-skills.mdc`（`alwaysApply`）+ 根目录 `AGENTS.md`，提示在匹配任务时读取 `.agent/skills/<id>/SKILL.md`。 |
| **其他 Agent** | 读 `AGENTS.md`，再按需打开对应 `SKILL.md`。 |

无法自动索引目录的环境，仍可用 **模式一** 手动 `@` 引用 `SKILL.md`。

## 目录导航

- `docs/ai-quickstart.md` — AI 最短上手路径
- `docs/how-other-ai-use-this-project.md` — 各工具接入说明
- `AGENTS.md` — 跨工具 Agent 入口
- `docs/agent-skill-rule-discovery.md` — 各平台 Skill / Rule 发现机制说明
- `docs/architecture.md` — Koi Python 服务端通用架构标准 (v4.0)
- `skeleton/` — 最小可运行项目骨架
- `examples/minimal-service/` — 最小结构样例
- `examples/device/` — 完整领域分层示例
- `examples/async-service/` — 完整异步路径示例
- `.agent/skills/` — 16 个 Skill 源码目录
- `.agent/skills/index.yaml` — 机器可读的 intent → skill 路由索引
- `scripts/` — 根级脚手架脚本

## 技术栈

- Python **3.13+**（本蓝图仅认证此版本线）
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
| `architecture-review` | 按 Koi 标准审查架构 |
| `testing-scaffold` | 补齐单元/集成测试骨架 |
| `auth-rbac-setup` | 补 JWT 鉴权与角色权限 |
| `production-hardening` | 做生产化加固与上线检查 |
| `async-upgrade` | 升级到异步架构路径 |
| `api-versioning` | 接口版本管理与迁移 |
| `rate-limit-setup` | 限流策略与 429 测试 |

## 开发建议

1. 先维护 `docs/architecture.md`
2. 再维护 `skeleton/`，确保 `pytest` 可通过
3. 再补充 `examples/`
4. 最后完善 `.agent/skills/` 中的脚本、模板与 references

## 贡献

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 安全

详见 [SECURITY.md](SECURITY.md)。

## 许可

[MIT](LICENSE) © mrkoi
