# koi_blueprint_python 修改与演进方案

本文档说明本蓝图仓库的**改进维度**、**与架构文档的对齐关系**，以及**当前实施状态与开放项**。技术细节以 `docs/architecture.md`（v4.0）为准。

---

## 1. 目的与范围

- **目的**：在「文档 → 骨架 → 示例 → Agent Skill」链路上保持可维护、可复现、可审计。
- **范围**：`docs/`、`skeleton/`、`examples/`、`.agent/skills/`、根级 CI 与脚本；不替代各业务项目自身的发布节奏说明。

---

## 2. 改进维度与条目

### 2.1 文档与示例一致性

| 目标 | 做法 |
|------|------|
| 架构文档中的代码块可直接复制运行 | 保持缩进与语法正确；示例与 `skeleton/` 行为一致 |
| 日志在进程早期初始化 | `create_app()` 内调用 `setup_logging()`；`lifespan` 仅管理长生命周期资源 |
| 集成测试与「最小骨架」策略一致 | 提供 `tests/integration/` 模板与注释；ORM 就绪后启用 `create_all` 等步骤 |

### 2.2 依赖与可复现构建

| 目标 | 做法 |
|------|------|
| 默认数据库 URL 与已声明驱动一致 | 使用 `postgresql+psycopg` 时，在 `pyproject.toml` 声明 `psycopg[binary]` 等 |
| 依赖可锁定 | 推荐在项目中执行 `uv lock` 并提交 `uv.lock`；镜像构建可与无 lock 的初始化阶段兼容（见 `skeleton/Dockerfile`） |

### 2.3 容器与 CI

| 目标 | 做法 |
|------|------|
| 构建失败可观测 | 避免静默忽略 `uv sync` 失败；多阶段构建、生产镜像精简 |
| 蓝图仓库可验证骨架 | 根级 CI 使用 `working-directory: skeleton`（或等价方式）跑 lint、类型检查、测试、安全扫描与 Docker 构建 |

### 2.4 测试与质量

| 目标 | 做法 |
|------|------|
| 集成测试有据可依 | `conftest` 中说明事务边界；与 `docs/architecture.md` 中 Testcontainers 示例对齐 |
| 测试分层可扩展 | 目录区分 `unit` / `integration`；在 `pyproject.toml` 注册 `pytest` markers |

### 2.5 Skill 与 Agent 体验

| 目标 | 做法 |
|------|------|
| Skill 与架构版本可追溯 | 各 `SKILL.md` 注明适配的 `docs/architecture.md` 主版本 |
| 安装路径可发现 | 根 `README` 说明 Codex / Cursor 路径；可选增加 `docs/` 专页深化 |
| 可选脚手架 | 可在不改主流程前提下增加 Copier / Cookiecutter，复用 `scripts/apply_skeleton.py` |

### 2.6 安全与可观测性（补充）

| 目标 | 做法 |
|------|------|
| 示例环境变量不误导生产 | `.env.example` 标明禁止用于生产的默认值 |
| 进阶可观测性 | 与 `add-observability` Skill、`architecture.md` 中 Out of Scope 章节呼应；可选独立短文 |

---

## 3. 当前实施状态（截至文档修订日）

以下基于仓库现状归纳，用于快速对齐「已落地 / 仍可选」。

### 3.1 已落实

| 维度 | 说明 |
|------|------|
| 文档示例 | `architecture.md` §4.2 等异常示例无破坏性笔误 |
| 骨架日志 | `skeleton/app/main.py` 在 `create_app()` 开头初始化日志 |
| 依赖 | `skeleton/pyproject.toml` 含 `psycopg[binary]` 等 |
| 镜像 | `skeleton/Dockerfile` 支持存在或缺失 `uv.lock` 的分支构建 |
| CI | 根 `.github/workflows/ci.yml` 在 `skeleton` 下执行质量门禁与 Docker 构建 |
| 测试 | `pytest` 已注册 `unit` / `integration`；含 coverage 与集成测试模板 |
| 安全示例 | `skeleton/.env.example` 含生产环境警示（中英） |
| Skill 版本 | **全部 9 个** SKILL.md 已标注适配 `docs/architecture.md` v4.0 |

### 3.2 开放项（非阻塞，按需排期）

| 项 | 说明 |
|----|------|
| `skeleton/uv.lock` | 推荐提交 lock 文件，与「确定性依赖」叙述完全一致 |
| `docs/skill-setup.md` | 可选：Skill 安装、软链、自检命令 |
| Copier / Cookiecutter | 可选：一键生成新项目 |
| 可观测性短文 | 可选：与 OTel / Prometheus 扩展互链 |

---

## 4. 建议执行顺序（面向后续迭代）

1. 维护 `docs/architecture.md` 与 `skeleton/` 行为一致（含示例与约束清单）。
2. 在骨架或模板项目中优先提交 `uv.lock`（若采用锁定策略）。
3. 按产品需要引入 Copier 或专页文档，不阻塞主线复制骨架流程。

---

## 5. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-03-21 | 初稿：审阅与 GitHub 同类项目比对 |
| 1.1 | 2026-03-21 | 多轮修复过程记录（已由 v2.0 合并吸收） |
| **2.0** | **2026-03-21** | **全文重新生成：合并改进项、实施状态与开放项，去除重复轮次章节** |

---

## 6. 署名

**编制：** Cursor AI 助手（与用户协作整理）  
**项目名称：** koi_blueprint_python  
**文档路径：** `docs/modification-plan.md`

---

*实施以实际 PR 与团队评审为准；开放项优先级由维护者按版本计划调整。*
