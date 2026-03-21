# 各平台 Skill / Rule 发现机制

本文说明常见 AI 编码工具如何发现 **项目级规则** 与 **Agent Skills**，以及本蓝图仓库（`koi_blueprint_python`）如何与各机制对齐。

> **本仓库的单一事实源**：`.agent/skills/<skill-id>/SKILL.md`（及同目录下的 `references/`、`scripts/`、`assets/`）。  
> `.agent/skills/index.yaml` 为机器可读路由索引；根目录 **`AGENTS.md`** 为跨工具的人类/Agent 索引；**`docs/architecture.md`** 为架构与工程约束的权威说明。

---

## 1. 概念区分

| 类型 | 典型作用 | 常见形态 |
|------|----------|----------|
| **Rules / Instructions** | 始终或按文件类型注入的约束（风格、安全、项目约定） | `AGENTS.md`、`.cursor/rules/*.mdc`、IDE 专有的 instructions 文件 |
| **Agent Skills** | 按需加载的工作流（脚手架、迁移、加固 checklist） | 目录包：`SKILL.md` + 可选脚本与参考文档 |

Skills 强调 **渐进披露**：先只索引轻量元数据（如 `description`），匹配用户意图后再加载完整正文，避免上下文膨胀。

---

## 2. 各平台发现机制（概览）

以下路径与行为以各工具**公开文档与常见约定**为准；具体版本请以官方说明为准。

| 平台 / 工具 | 规则 / 说明类 | Skills / 专项能力 |
|---------------|---------------|-------------------|
| **Google Antigravity** | 根目录可配合 **`AGENTS.md`**（跨工具说明）；Antigravity 另有 **`GEMINI.md`** 仅作用于本工具，若与 `AGENTS.md` 并存，**以 `GEMINI.md` 为准**（用于 Antigravity 专属覆盖） | **工作区级**：`.agent/skills/<name>/`（`SKILL.md` 为入口）；**用户全局**：`~/.gemini/antigravity/skills/`（官方 Codelab 约定） |
| **OpenAI Codex（CLI / IDE）** | 仓库根目录 **`AGENTS.md`** 为常见项目级入口（工具版本不同，加载策略可能略有差异） | 部分环境使用 **`$CODEX_HOME/skills/`** 等全局目录；可将本仓库 `.agent/skills/*` **软链接或复制**到该目录作为可选增强 |
| **Cursor** | **`.cursor/rules/*.mdc`**（YAML frontmatter：`description`、`globs`、`alwaysApply` 等） | 无独立「Skill 目录」标准；通过 Rule 提示 Agent **读取** `.agent/skills/<id>/SKILL.md` |
| **Claude Code** | 根目录 **`CLAUDE.md`**（及子目录）为常见约定；部分生态使用 **`.claude/skills/`** 存放技能包 | 项目级 skills 目录因工具链而异，本蓝图以 **`.agent/skills/`** 为统一副本，Claude 可通过读 `AGENTS.md` 再打开对应 `SKILL.md` |
| **GitHub Copilot** | **`.github/copilot-instructions.md`**（或 Settings 中的自定义 instructions） | 不定义与本仓库相同的 Skill 目录标准；需显式引用文件 |
| **Windsurf** | **`.windsurfrules`** 或 **`.windsurf/rules/`** 等（以当前 IDE 文档为准） | 同 Cursor：用规则文件指向仓库内 `SKILL.md` |

---

## 3. 本仓库的对齐方式

### 3.1 与 Antigravity 对齐

- Google Antigravity 官方 Codelab 约定：**工作区 Skill** 位于 **`.agent/skills/`**，与本仓库目录结构一致。
- 每个 Skill 的 **`SKILL.md`** 使用 YAML frontmatter（`name`、`description`），`description` 用于 Agent **语义路由**。
- 若需仅 Antigravity 生效的补充说明，可使用根目录 **`GEMINI.md`**；注意与 **`AGENTS.md`** 的优先级关系，避免无意覆盖团队共识。

### 3.2 与 Codex 对齐

- 使用根目录 **`AGENTS.md`** 列出必读文档与 Skill 索引表。
- 若 Codex 环境要求技能出现在全局目录，可将 **`.agent/skills/*`** 链到 **`$CODEX_HOME/skills/`**；**Git 中的权威副本仍为 `.agent/skills/`**。

### 3.3 与 Cursor 对齐

- **`.cursor/rules/koi-agent-skills.mdc`**：`alwaysApply: true` 时，在对话中持续提示：当用户任务匹配某类场景时，读取 **`.agent/skills/<skill-id>/SKILL.md`** 并按步骤执行。
- 与 **`AGENTS.md`** 互补：**不重复粘贴**每个 Skill 的全文，避免多处维护。

### 3.4 无法自动发现目录的环境

- 使用 **知识库模式**：先读 `docs/ai-quickstart.md`，再让 Agent 阅读 `README.md`、`docs/architecture.md`，并对具体任务 **`@` 引用** 某个 `SKILL.md` 路径。

---

## 4. 本仓库文件一览（与发现机制相关）

| 路径 | 用途 |
|------|------|
| `docs/ai-quickstart.md` | 给 AI 的极简入口：最短读取顺序、全局约束、默认路由方式 |
| `docs/how-other-ai-use-this-project.md` | 面向 Claude / Copilot / Cursor / Windsurf 的接入示例与推荐提示词 |
| `AGENTS.md` | 跨工具 Agent 入口：必读、Skill 索引、Codex 全局目录说明 |
| `.cursor/rules/koi-agent-skills.mdc` | Cursor Rule：提示按任务加载对应 `SKILL.md` |
| `.agent/skills/index.yaml` | 机器可读的 intent → skill 路由索引 |
| `.agent/skills/<skill-id>/SKILL.md` | 各 Skill 正文与步骤（单一事实源） |
| `docs/architecture.md` | 架构与工程规范（非 Skill 流程细节） |
| `docs/agent-skill-rule-discovery.md` | 本文：各平台发现机制说明 |

---

## 5. 维护建议

1. 新增或重命名 Skill 时：同步更新 **`AGENTS.md`** 与 **`.cursor/rules/koi-agent-skills.mdc`** 中的索引表（保持两边一致）。
2. Skill 正文只改 **`.agent/skills/.../SKILL.md`**，避免在 Rule 里复制大段流程。
3. 若引入 **`GEMINI.md`**，仅写入 Antigravity 专属差异，并避免与 `AGENTS.md` 中的团队级约束冲突。

---

## 6. 参考

- Google Codelabs：*Authoring Google Antigravity Skills*（工作区 `.agent/skills/`、全局 `~/.gemini/antigravity/skills/`）
- 本仓库：`README.md`（模式一 / 模式二）、`CONTRIBUTING.md`（变更顺序）
