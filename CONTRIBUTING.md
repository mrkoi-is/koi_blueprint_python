# Contributing to koi_blueprint_python

感谢你对本项目的贡献！/ Thank you for contributing!

## 开发流程 / Development Workflow

### 1. 克隆与设置

```bash
git clone https://github.com/mrkoi-is/koi_blueprint_python.git
cd koi_blueprint_python
```

### 2. 修改优先级

1. 先维护 `docs/architecture.md`
2. 若变更影响 Agent 行为或 Skill 索引，同步更新根目录 `AGENTS.md`、`docs/agent-skill-rule-discovery.md`（与 `.cursor/rules/` 保持叙述一致）
3. 再维护 `skeleton/`，确保 `pytest` 可通过
4. 再补充 `examples/`
5. 最后完善 `.agent/skills/` 中的脚本、模板与 references

### 3. 代码质量

所有提交必须通过:

```bash
cd skeleton
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

### 4. 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — 新特性
- `fix:` — Bug 修复
- `docs:` — 文档更新
- `refactor:` — 代码重构
- `chore:` — 构建/工具链变更

### 5. Pull Request

- 确保所有 CI 检查通过
- 描述清楚修改动机和影响范围
- 如涉及架构变更，先更新 `docs/architecture.md`
