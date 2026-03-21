# koi_blueprint_python

面向 AI Agent 的 Python 服务端架构蓝图仓库。

这个仓库的目标是让 AI 用统一方式生成符合 Koi 标准的 Python 服务端项目。它同时提供：

- `docs/architecture.md`：通用架构规范
- `skeleton/`：可直接复制的最小可运行骨架
- `examples/`：最小服务与领域模块示例
- `.agent/skills/`：可安装或可直接阅读的 Skill 源码

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

- `docs/architecture.md`：Koi Python 服务端通用架构标准
- `skeleton/`：最小可运行项目骨架
- `examples/minimal-service/`：最小可运行金样例
- `examples/device/`：完整领域模块示例
- `.agent/skills/`：Skill 源码目录

## 技术栈

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- uv
- Ruff
- pyright
- structlog
- Testcontainers

## 开发建议

1. 先维护 `docs/architecture.md`
2. 再维护 `skeleton/`，确保 `pytest` 可通过
3. 再补充 `examples/`
4. 最后完善 `.agent/skills/` 中的脚本、模板与 references
