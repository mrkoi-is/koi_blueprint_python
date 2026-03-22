# Contributing to koi_blueprint_python

感谢你对本项目的贡献！/ Thank you for contributing!

## Development Workflow / 开发流程

### 1. Clone / 克隆与设置

```bash
git clone https://github.com/mrkoi-is/koi_blueprint_python.git
cd koi_blueprint_python
```

### 2. Priority Order / 修改优先级

1. 先维护 `docs/architecture.md` / Maintain architecture doc first
2. 若变更影响 Agent 行为或 Skill 索引，同步更新根目录 `AGENTS.md`、`docs/agent-skill-rule-discovery.md`（与 `.cursor/rules/` 保持叙述一致）
3. 再维护 `skeleton/`，确保 `pytest` 可通过 / Then skeleton, ensure pytest passes
4. 再补充 `examples/` / Then examples
5. 最后完善 `.agent/skills/` 中的脚本、模板与 references / Finally Skills

### 3. Code Quality / 代码质量

所有提交必须通过 / All commits must pass:

```bash
cd skeleton
uv sync --all-groups
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest
```

### 4. Commit Convention / 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — 新特性 / New feature
- `fix:` — Bug 修复 / Bug fix
- `docs:` — 文档更新 / Documentation update
- `refactor:` — 代码重构 / Refactor
- `chore:` — 构建/工具链变更 / Build/toolchain change

### 5. Pull Request

- 确保所有 CI 检查通过 / Ensure all CI checks pass
- 描述清楚修改动机和影响范围 / Describe motivation and scope clearly
- 如涉及架构变更，先更新 `docs/architecture.md` / Update architecture doc for arch changes

## Contributing a Skill / 贡献新 Skill

AI Agent Skills 是本项目最核心的贡献路径。  
AI Agent Skills are the most impactful contribution path for this project.

### Skill Structure / Skill 结构

```
.agent/skills/<skill-id>/
├── SKILL.md             # 入口（YAML frontmatter: name, description）
├── references/          # 参考文档、checklist
├── scripts/             # 辅助脚本（可选）
└── templates/           # 代码模板（可选）
```

### Steps / 步骤

1. **Create directory** / 创建目录：`.agent/skills/<your-skill-id>/`
2. **Write `SKILL.md`** with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-id
   description: One-line description for agent routing.
   ---
   ```
3. **Update `.agent/skills/index.yaml`** — 添加 intent → skill 映射
4. **Update `AGENTS.md`** — 在 Skill 索引表中添加新行
5. **Update `README.md`** — 在 Skills 表格中添加新行
6. **Test** — 确保 Skill 指令可被 AI Agent 正确执行

### Guidelines / 指导原则

- Skill 正文应可被 AI Agent 直接执行（清晰、自包含）
- 参考 `docs/architecture.md` 确保输出代码符合 Koi 标准
- 提供 `references/` 下的 checklist 帮助 AI 做自检

