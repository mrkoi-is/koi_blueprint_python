# Koi Python 蓝图 — Agent 说明

本文件供 **Antigravity、OpenAI Codex（CLI/IDE）、Claude Code、Cursor** 等工具在仓库根目录自动加载，与 `.agent/skills/` 配合使用。

各工具如何发现 Rule / Skill 的**机制说明**见：`docs/agent-skill-rule-discovery.md`。

如需给 Claude、Copilot、Cursor、Windsurf 等工具单独提供接入提示，可参考：`docs/how-other-ai-use-this-project.md`。

## 必读

- AI 最短入口：`docs/ai-quickstart.md`
- 架构与约束：`docs/architecture.md`
- Python：**仅 3.13+**（`requires-python >= 3.13`）
- 骨架与示例：`skeleton/`、`examples/`

## Agent Skills（单一事实源）

- **位置**：`.agent/skills/<skill-id>/`
- **机器索引**：`.agent/skills/index.yaml`（供弱模型或工具先做 intent → skill 路由）
- **入口**：每个 Skill 的根文件为 `SKILL.md`（含 YAML frontmatter：`name`、`description`）。
- **Antigravity**：官方约定工作区级 Skill 即放在 **`.agent/skills/`**（与本仓库一致），由 Agent 按需索引 `description` 并加载正文。
- **其他工具**：若无法自动索引目录，请在用户任务与下表匹配时 **主动读取** 对应 `SKILL.md` 并按步骤执行。

### Skill 索引（任务 → 目录）

| 用户意图（示例） | Skill 目录 |
|------------------|------------|
| 新项目 / 从 skeleton 初始化 / bootstrap | `server-init` |
| 新领域模块 / domain / router+service+repo | `add-domain-module` |
| 基础设施适配器 / Redis / S3 / 外部 SDK | `add-infra-adapter` |
| Alembic / 迁移 / revision | `alembic-migration` |
| GitHub Actions / CI | `ci-setup` |
| Docker / compose / 部署资产 | `docker-deploy` |
| 后台任务 / Celery / ARQ / BackgroundTasks | `add-background-task` |
| WebSocket | `add-websocket` |
| 指标 / 追踪 / Prometheus / OpenTelemetry | `add-observability` |
| 架构评审 / 对照 Koi 规范 | `architecture-review` |
| 测试布局 / pytest / 单测与集成 | `testing-scaffold` |
| JWT / RBAC / 鉴权 | `auth-rbac-setup` |
| 生产加固 / 上线检查 | `production-hardening` |
| 同步改异步 / async 升级 | `async-upgrade` |
| API 版本 / v1 v2 / 弃用头 | `api-versioning` |
| 限流 / slowapi / 429 | `rate-limit-setup` |

执行顺序建议：先读 `SKILL.md` → 再读其 `references/` → 再运行其 `scripts/`（若有）→ 最后改业务代码并跑 `ruff` / `pyright` / `pytest`。

## Codex 全局 Skill 目录（可选）

若你的环境要求 Skill 出现在 **`$CODEX_HOME/skills/`**（或工具文档中的全局路径），可将本仓库的 `.agent/skills/*` **软链接或复制**到该目录；**本仓库仍以 `.agent/skills/` 为权威副本**，发布以 Git 为准。

## Cursor

本仓库包含 `.cursor/rules/`，用于在 Cursor 中提示加载上述 Skill；与 `AGENTS.md` 内容互补，不重复维护 Skill 正文。
