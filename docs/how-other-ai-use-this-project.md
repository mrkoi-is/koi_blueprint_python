# How Other AI Use This Project

> 面向 Claude、Copilot、Cursor、Windsurf、通用 Agent 的接入说明。目标是让不同 AI **用同一套路由方式**理解并使用本仓库。

## 1. 最短原则

无论使用哪一种 AI，优先遵循同一条最短路径：

1. 先读 `docs/ai-quickstart.md`
2. 再读 `AGENTS.md`
3. 再读 `.agent/skills/index.yaml`
4. 根据任务只加载对应的 `.agent/skills/<skill-id>/SKILL.md`
5. 只有在需要时再读该 Skill 的 `references/`、`scripts/`、`assets/`
6. 只有在涉及架构基线时，再读 `docs/architecture.md`、`skeleton/`、`examples/`

## 2. 通用提示词模板

把下面这段作为通用起始提示，适合大多数 AI：

```text
请先阅读 docs/ai-quickstart.md、AGENTS.md 和 .agent/skills/index.yaml。
根据当前任务选择最匹配的 Skill，只加载对应的 .agent/skills/<skill-id>/SKILL.md。
如果需要更多细节，再读取该 Skill 的 references/、scripts/、assets/。
除非任务涉及架构基线，否则不要一开始加载整个 docs/architecture.md 和全部 examples/。
```

## 3. Claude Code

### 推荐读取顺序

- `docs/ai-quickstart.md`
- `AGENTS.md`
- `.agent/skills/index.yaml`
- 对应 Skill 的 `SKILL.md`

### 推荐提示词

```text
请把这个仓库当作一个 AI-first Python blueprint。
先读 docs/ai-quickstart.md、AGENTS.md、.agent/skills/index.yaml，
然后按任务选择对应的 .agent/skills/<skill-id>/SKILL.md 并严格按 workflow 执行。
```

### 适用说明

- Claude Code 更适合按文件显式读取。
- 如果未来仓库增加 `CLAUDE.md`，它应只保留 Claude 专属差异，不要复制 Skill 正文。

## 4. GitHub Copilot

### 推荐方式

Copilot 没有与本仓库完全对齐的 Skill 目录标准，因此建议：

- 在对话里显式贴出要读的文件路径
- 先让它读 `docs/ai-quickstart.md`
- 再指定某个 `SKILL.md`

### 推荐提示词

```text
Read docs/ai-quickstart.md and AGENTS.md first.
Then open .agent/skills/index.yaml and choose the best matching skill for this task.
Only read the matching .agent/skills/<skill-id>/SKILL.md instead of the whole repository.
```

### 注意

- Copilot 容易默认从最近打开的代码推断实现，必要时要重复强调“先读 Skill，再动代码”。

## 5. Cursor

### 推荐方式

- 本仓库已提供 `.cursor/rules/koi-agent-skills.mdc`
- Cursor 会持续收到“按任务读取 `.agent/skills/<skill-id>/SKILL.md`”的提示
- 你仍然可以在对话中明确指定 Skill，减少歧义

### 推荐提示词

```text
Use the Koi project rules in this repo.
Match this task against .agent/skills/index.yaml and load only the most relevant SKILL.md.
Follow the skill workflow before editing files.
```

### 最佳实践

- 复杂任务先让 Cursor 读 `docs/ai-quickstart.md`
- 再明确任务类型，例如“这是 add-domain-module 场景”

## 6. Windsurf

### 推荐方式

Windsurf 没有与本仓库完全一致的 Skill 目录约定，建议按通用 Agent 模式使用：

- 先读 `docs/ai-quickstart.md`
- 再读 `AGENTS.md`
- 再读 `.agent/skills/index.yaml`
- 手动指定对应 `SKILL.md`

### 推荐提示词

```text
Treat this repository as an AI-oriented backend blueprint.
Read docs/ai-quickstart.md, AGENTS.md, and .agent/skills/index.yaml first.
Pick the most relevant skill and follow its workflow before making changes.
```

## 7. 通用 Agent / 内部平台 Agent

如果你的 Agent 不支持规则自动发现，建议直接把下面流程写进 system prompt 或 task preamble：

```text
This repository uses AGENTS.md + .agent/skills/index.yaml for routing.
Always read docs/ai-quickstart.md first.
Then map the user intent to a single skill under .agent/skills/ and load its SKILL.md.
Read references only when needed. Prefer skeleton/ over examples/ when generating standard code.
```

## 8. 常见任务与建议输入

### 新项目初始化

```text
请先读 docs/ai-quickstart.md、AGENTS.md、.agent/skills/index.yaml，
然后使用 server-init 对当前目录初始化一个符合 Koi 标准的新项目。
脚本 scripts/apply_skeleton.py 会同时复制骨架代码和 AI 工具链资产。
初始化完成后，确认新项目中包含 AGENTS.md、.agent/skills/、.cursor/rules/、docs/architecture.md。
```

### 新增业务模块

```text
请按 add-domain-module 的 workflow，在当前服务中新增一个领域模块。
先读 docs/ai-quickstart.md、AGENTS.md、.agent/skills/index.yaml，再读对应 SKILL.md。
```

### 审核项目

```text
请按 architecture-review 的 workflow 审核当前项目。
先读 docs/ai-quickstart.md、AGENTS.md、.agent/skills/index.yaml，再输出问题、优先级和修复建议。
```

### Docker / CI / 可观测性

```text
请先按 docs/ai-quickstart.md 的最短路径路由到合适 Skill，
再分别使用 docker-deploy / ci-setup / add-observability 的 workflow 做修改。
```

## 9. 不同 AI 的统一约束

所有 AI 都应遵守以下约束：

- Python 版本线固定为 `3.13+`
- 标准实现优先参考 `skeleton/`
- `examples/` 更偏示例，不优先于 `skeleton/`
- Skill 单一事实源是 `.agent/skills/<skill-id>/SKILL.md`
- 复杂任务不要一次性把 16 个 Skill 全部读入上下文
- 修改后尽量执行项目标准校验，如 `ruff`、`pyright`、`pytest`

## 10. 推荐维护方式

如果未来要继续增强“其他 AI 如何使用本项目”，建议遵循：

- 优先更新 `docs/ai-quickstart.md`
- 再更新 `.agent/skills/index.yaml`
- 再更新本文件中的具体示例提示词
- 最后才更新 `AGENTS.md` / `README.md` 中的目录导航说明

这样可以保持：
- 极简入口稳定
- 机器索引稳定
- 跨工具示例说明独立演进
