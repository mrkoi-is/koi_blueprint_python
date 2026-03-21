# Skill 升级修复报告

> 生成时间：2026-03-21  
> 范围：统一 Skill 版本口径、补齐弱项 Skill 资源、并将旧 Skill 改写为新模板风格。

## 本轮完成项

### 1. 版本口径统一

- 将 `README.md` 中 `.agent/skills/` 的说明统一为：当前 Skill 全部按 `docs/architecture.md` `v4.0` 维护。
- 将 `README.md` 中 `docs/architecture.md` 的版本展示从 `v0.0.1，草案` 统一为 `v4.0`。
- 本轮改写后的 16 个 Skill 已统一采用 `> 适配 \`docs/architecture.md\` v4.0` 的标注口径。

### 2. 三个弱项 Skill 升级

已升级：
- `.agent/skills/add-background-task/`
- `.agent/skills/add-observability/`
- `.agent/skills/add-websocket/`

修复内容：
- 补齐 `agents/openai.yaml`
- 补齐 `references/`
- 将原先堆在 `SKILL.md` 中的长代码块下沉到 `references/`
- `add-observability` 额外补齐：
  - `assets/docker-compose.observability.template.yml`
  - `assets/prometheus.yml`
  - `scripts/inspect_observability_surface.py`
- 为统一检查体验，额外补齐：
  - `add-background-task/scripts/inspect_background_task_surface.py`
  - `add-websocket/scripts/inspect_websocket_surface.py`

### 3. 六个旧 Skill 统一为新模板

已统一改写：
- `.agent/skills/server-init/SKILL.md`
- `.agent/skills/add-domain-module/SKILL.md`
- `.agent/skills/add-infra-adapter/SKILL.md`
- `.agent/skills/alembic-migration/SKILL.md`
- `.agent/skills/ci-setup/SKILL.md`
- `.agent/skills/docker-deploy/SKILL.md`

统一后的结构包含：
- 版本标记
- `Use this skill when...`
- `Workflow`
- `Principles / Rules`
- 对 `references/`、`scripts/`、`assets/` 的显式引用

### 4. 第二轮统一优化

- 将 6 个旧 Skill 对应的 `references/` 从“极简列表”补为结构化清单，提升可执行性与一致性。
- 为全部 `agents/openai.yaml` 显式补齐 `policy.allow_implicit_invocation: true`，统一 UI/路由元数据口径。
- 为 `add-background-task`、`add-websocket` 新增检查脚本，使其与 `architecture-review`、`testing-scaffold`、`add-observability` 的风格更一致。

### 5. AI 入口与目录噪音优化

- 新增 `docs/ai-quickstart.md`，为弱模型和普通 Agent 提供最短读取路径。
- 新增 `docs/how-other-ai-use-this-project.md`，为 Claude / Copilot / Cursor / Windsurf 提供可直接复用的接入提示词。
- 新增 `.agent/skills/index.yaml`，提供机器可读的 `intent -> skill` 路由索引。
- 新增 `.ignore`，并补充 `.gitignore` / `skeleton/.gitignore` 中的 `.tmp/` 忽略规则。
- 清理仓库中的 `__pycache__`、`.ruff_cache`、`.pytest_cache` 等缓存目录，降低 AI 搜索噪音。

## 新增资源清单

### add-background-task

- `agents/openai.yaml`
- `references/strategy-guide.md`
- `references/fastapi-backgroundtasks-patterns.md`
- `references/queue-worker-patterns.md`
- `scripts/inspect_background_task_surface.py`

### add-observability

- `agents/openai.yaml`
- `references/metrics-checklist.md`
- `references/tracing-checklist.md`
- `assets/docker-compose.observability.template.yml`
- `assets/prometheus.yml`
- `scripts/inspect_observability_surface.py`

### add-websocket

- `agents/openai.yaml`
- `references/websocket-patterns.md`
- `references/websocket-auth-and-testing.md`
- `scripts/inspect_websocket_surface.py`

### 通用 AI 入口

- `docs/ai-quickstart.md`
- `docs/how-other-ai-use-this-project.md`
- `.agent/skills/index.yaml`
- `.ignore`

## 验证结果

本轮已完成以下校验：

- `python3 -m compileall -q .agent/skills` ✅
- 通过临时虚拟环境执行 `ruff check .agent/skills` ✅
- 已确认 16 个 Skill 全部具备 `SKILL.md` ✅
- 已确认 `add-background-task`、`add-observability`、`add-websocket` 全部具备 `agents/openai.yaml` ✅
- 已确认全部 Skill 的 `agents/openai.yaml` 已显式补齐 `policy.allow_implicit_invocation: true` ✅
- 已执行：
  - `add-background-task/scripts/inspect_background_task_surface.py` ✅
  - `add-websocket/scripts/inspect_websocket_surface.py` ✅
  - `add-observability/scripts/inspect_observability_surface.py` ✅
- 已确认 `docs/ai-quickstart.md` 与 `.agent/skills/index.yaml` 已接入仓库入口说明 ✅
- 已确认 `docs/how-other-ai-use-this-project.md` 已接入仓库导航与发现说明 ✅

## 结果

本轮修复后，Skill 体系已从“部分新、部分旧、部分只有说明文本”的状态，收敛为：

- 版本口径统一
- 资源分层更清晰
- 弱项 Skill 不再把实现细节全部塞进 `SKILL.md`
- 旧 Skill 与新 Skill 的写法风格基本一致
