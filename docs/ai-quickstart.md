# AI Quickstart

> 给 AI Agent 的最短上手路径。目标是**少读文件、快速路由、减少上下文膨胀**。

## 1. 最小读取顺序

按下面顺序读取，**不要一开始就把整个仓库全部读完**：

1. `docs/ai-quickstart.md`
2. `AGENTS.md`
3. `.agent/skills/index.yaml`
4. 按任务匹配到的单个 `SKILL.md`
5. 只有在需要时再读该 Skill 的 `references/`、`scripts/`、`assets/`
6. 只有在修改架构、骨架或示例时，再读：
   - `docs/architecture.md`
   - `skeleton/`
   - `examples/`

## 2. 全局硬约束

- Python 版本线：`3.13+`
- Web 框架基线：`FastAPI + Pydantic v2`
- Skill 单一事实源：`.agent/skills/<skill-id>/SKILL.md`
- 架构权威说明：`docs/architecture.md`
- 生成或修复代码时，优先复用 `skeleton/` 和根级 `scripts/`

## 3. 路由规则

- 先读 `.agent/skills/index.yaml`，根据 `intent` / `keywords` 选择 Skill。
- 只加载**当前任务需要的一个或少数几个 Skill**，不要把 16 个 Skill 全部读入上下文。
- 如果工具不支持自动发现 Skill，手动打开对应 `.agent/skills/<skill-id>/SKILL.md`。

## 4. 常见任务 → Skill

- 新项目初始化：`server-init`
- 新领域模块：`add-domain-module`
- 基础设施适配器：`add-infra-adapter`
- 数据库迁移：`alembic-migration`
- CI：`ci-setup`
- Docker / 部署：`docker-deploy`
- 后台任务：`add-background-task`
- WebSocket：`add-websocket`
- 可观测性：`add-observability`
- 架构审查：`architecture-review`
- 测试补齐：`testing-scaffold`
- JWT / RBAC：`auth-rbac-setup`
- 生产加固：`production-hardening`
- 异步升级：`async-upgrade`
- API 版本管理：`api-versioning`
- 限流：`rate-limit-setup`

## 5. 推荐执行顺序

对任一 Skill，优先按以下顺序工作：

1. 读 `SKILL.md`
2. 读该 Skill 的 `references/`
3. 运行该 Skill 的 `scripts/`（如有）
4. 再修改业务代码
5. 最后执行项目校验（如 `ruff`、`pyright`、`pytest`）

## 6. 读代码时的优先级

### 如果你在做“标准实现”

优先读：
- `skeleton/`
- 根级 `scripts/`
- `docs/architecture.md`

### 如果你在做“参考对照”

再读：
- `examples/`

> `examples/` 更偏参考，不应优先于 `skeleton/` 作为标准输出来源。

## 7. 避免的行为

- 不要把所有 Skill 一次性读进上下文。
- 不要优先从 `examples/` 复制实现，除非任务明确要求参考示例。
- 不要忽略 `AGENTS.md` 和 `.agent/skills/index.yaml` 自己猜目录语义。
- 不要在仓库缓存目录中搜索证据；这些目录已经被忽略。
