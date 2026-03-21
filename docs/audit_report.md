# koi_blueprint_python 深度审计报告 / Deep Audit Report

> 审计时间: 2026-03-21 | 审计范围: 架构、代码、工具链、Skills、CI/CD、安全性、可观测性
> Audit Date: 2026-03-21 | Scope: Architecture, Code, Tooling, Skills, CI/CD, Security, Observability

---

## 1. 竞品对标 / Comparable GitHub Projects

以下是当前 GitHub 上最具代表性的 FastAPI 企业级模板/架构项目：

| 项目 | ⭐ Stars | 核心特色 | 与 Koi 差异 |
|---|---|---|---|
| **fastapi-practices/fastapi-best-architecture** | 5k+ | Celery、Casbin RBAC、Grafana、pseudo-3-tier、uv+Ruff | 可观测性、后台任务、RBAC 均内置 |
| **iam-abbas/FastAPI-Production-Boilerplate** | 1k+ | Row-Level Access Control、Celery、SQLAlchemy 2.0、完整 CRUD 封装 | 内置 CRUD 基类、后台任务 |
| **one-zero-eight/fastapi-template** | 300+ | Cookiecutter 生成器、pre-commit、Python 3.13、uv+Ruff、GitHub Actions | Cookiecutter 模板化生成、pre-commit hooks |
| **n0nuser/fastapi-archetype** | 28+ | DDD、Best Docker、Bandit 安全扫描、多 lint 工具 | 安全扫描(Bandit)、更严格 lint |
| **NEONKID/fastapi-ddd-example** | 326+ | DDD + Protocol-based interfaces、SQLAlchemy、explicit DI | 用 `Protocol` 代替 `ABC`（更 Pythonic） |
| **fastapi-clean-architecture-ddd-template** | 200+ | Clean Architecture 4 层、DI via Depends、明确 Application 层 | 显式 Application Layer (Use Case) |

---

## 2. 总体评价 / Overall Assessment

> [!TIP]
> **Koi Blueprint 已具备一个高质量企业模板的坚实基础**。架构文档详尽(981行)，技术栈选型（Astral 工具链、FastAPI、SQLAlchemy 2.0 Mapped、structlog、Testcontainers）处于 2026 Python 生态前沿，领域目录结构清晰，Agent Skill 系统是独特差异化优势。

### ✅ 做得好的部分

| 领域 | 评价 |
|---|---|
| **架构文档** | 981 行覆盖技术栈、目录结构、代码模式、约束清单，在同类项目中**最详尽** |
| **Astral 工具链** | uv + Ruff + pyright 是 2026 最佳实践，优于多数竞品仍在用 Poetry + black + mypy |
| **分层约束** | Router → Service → Repository + UoW 依赖倒置，架构约束清单(§8)可操作 |
| **Agent Skill 系统** | 6 个 Skill 是独特差异化（竞品无此功能），定位 "AI-native template" |
| **Dockerfile** | 多阶段构建 + uv + HEALTHCHECK，精简且高效 |
| **异常体系** | AppError 层次 + 全局处理器 + 统一 JSON 格式，完整且实用 |

---

## 3. 优化空间总览 / Optimization Opportunities Summary

| # | 分类 | 严重程度 | 优化项 |
|---|---|---|---|
| 1 | 🏗️ 架构 | 🔴 高 | 缺少 Base Model / CRUD 基类，每个领域要重复大量样板代码 |
| 2 | 🏗️ 架构 | 🔴 高 | 缺少异步 (async) 完整路径，架构文档提及但 skeleton 全同步 |
| 3 | 🏗️ 架构 | 🟡 中 | 缺少 Application Layer (Use Case)，Service 直接处理所有业务逻辑 |
| 4 | 🛡️ 安全 | 🔴 高 | 无安全扫描工具(Bandit/Safety)，无 Rate Limiting，JWT 无 exp/iss 检查 |
| 5 | 📊 可观测性 | 🔴 高 | 无 Metrics(Prometheus)、无 Tracing(OpenTelemetry) 支持 |
| 6 | ⏱️ 后台任务 | 🟡 中 | 缺少 Celery / ARQ / 后台任务基础设施 |
| 7 | 🧪 测试 | 🔴 高 | skeleton 只有 1 个 test_health，无 unit/integration 示范测试 |
| 8 | 🔧 工具链 | 🟡 中 | 缺少 pre-commit hooks |
| 9 | 🔧 工具链 | 🟡 中 | Dockerfile 缺少 `uv.lock`、`--frozen` flag 已在架构文档中但 skeleton 未用 |
| 10 | 🔧 工具链 | 🟢 低 | CI 缺少 coverage 报告、安全扫描 step |
| 11 | 📁 Skill | 🟡 中 | 所有 Skill 引用的 `scripts/` 和 `references/` 目录不存在 |
| 12 | 📁 Skill | 🟡 中 | 缺少常用 Skill: `add-background-task`、`add-websocket`、`add-middleware` |
| 13 | 📁 结构 | 🟡 中 | skeleton 缺少 `docker-compose.yml` 本地开发编排 |
| 14 | 📁 结构 | 🟢 低 | 缺少 `CONTRIBUTING.md`、`CHANGELOG.md` |
| 15 | 🏗️ 架构 | 🟢 低 | [dependencies.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/dependencies.py) 模块级创建 engine，不在 Lifespan 管理 |
| 16 | 🏗️ 架构 | 🟡 中 | Repository 用 ABC 而非 Protocol，竞品趋势是 Protocol |
| 17 | 📁 结构 | 🟢 低 | skeleton 缺 [alembic.ini](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/alembic.ini) 对应的 `migrations/env.py` 实例代码 |

---

## 4. 详细分析 / Detailed Analysis

### 4.1 🏗️ 架构层优化 / Architecture

#### 4.1.1 缺少 Base Model & Generic CRUD Repository (🔴 高)

**问题**: 每个领域模块的 [repository.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/examples/device/repository.py) 和 [repository_sa.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/examples/device/repository_sa.py) 需要手写 `get_by_id`, `add`, `list_all`, `count`, `delete` 等几乎相同的方法，导致大量重复代码。

**竞品做法**:
- `fastapi-best-architecture`: 提供 `CRUDBase[ModelType]` 泛型基类，内含通用 CRUD
- `iam-abbas/FastAPI-Production-Boilerplate`: 提供 `BaseRepository` + `ReadOnlyRepository`

**建议**: 添加 `app/core/repository.py`:
```python
# 泛型 CRUD 基类
class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: int) -> T | None: ...
    @abstractmethod
    def add(self, entity: T) -> None: ...
    @abstractmethod
    def list(self, offset: int, limit: int) -> list[T]: ...
    @abstractmethod
    def count(self) -> int: ...
    @abstractmethod
    def delete(self, entity: T) -> None: ...

class SaRepository(AbstractRepository[T]):
    """SQLAlchemy 通用实现，减少 80%+ 样板代码"""
    def __init__(self, session: Session, model_class: type[T]):
        self._session = session
        self._model_class = model_class
    # ... 通用实现
```

#### 4.1.2 missing async 完整路径 (🔴 高)

**问题**: 架构文档 §2.3 详细讨论了 sync/async 策略，但 skeleton 全部是同步代码。[dependencies.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/dependencies.py) 使用同步 `create_engine` 和 `Session`。对于需要 async 的项目，无现成的异步骨架可用。

**建议**:
- 在 skeleton 或 examples 中提供 async 变体: `AsyncSession`, `create_async_engine`, `asyncpg`
- 或创建新 Skill: `convert-to-async`

#### 4.1.3 Protocol vs ABC (🟡 中)

**问题**: 当前 Repository 接口用 `ABC`。Python 3.12+ 社区趋势是使用 `Protocol`（结构化子类型），更 Pythonic、无需继承。

**竞品做法**: `NEONKID/fastapi-ddd-example` 使用 `Protocol` 定义 Repository 接口。

**建议**: 升级至 `Protocol`:
```python
class DeviceRepository(Protocol):
    def get_by_sn(self, sn: str) -> Device | None: ...
    def add(self, device: Device) -> None: ...
```

#### 4.1.4 Engine 在模块级创建 (🟢 低)

**问题**: [dependencies.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/dependencies.py) 在模块顶层 `engine = create_engine(settings.database_url)` 创建引擎，这意味着 import 时即创建连接池，不在 Lifespan 管理中。测试时可能引起连接泄漏。

**建议**: 将 engine 创建移到 [lifespan()](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/main.py#15-19) 中或使用延迟初始化模式。

---

### 4.2 🛡️ 安全性 / Security

#### 4.2.1 缺少安全扫描工具 (🔴 高)

**问题**: 无 Bandit（代码安全审计）、无 Safety/pip-audit（依赖漏洞扫描）。

**竞品做法**: `n0nuser/fastapi-archetype` 内置 Bandit 配置。

**建议**:
```toml
# pyproject.toml 添加
[dependency-groups]
dev = [
    "bandit>=1.8",
    "pip-audit>=2.7",
]
```
```makefile
# Makefile 添加
security:  ## 安全扫描
	uv run bandit -r app/
	uv run pip-audit
```

#### 4.2.2 JWT 缺少生产级检查 (🔴 高)

**问题**: [auth.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/auth.py) 的 `jwt.decode()` 只指定 `algorithms=["HS256"]`，未验证 `exp`（过期时间）、`iss`（签发者）、`aud`（受众）。架构文档 §4.4 末尾有提及但 skeleton 代码未实现。

**建议**: 在 skeleton 中至少加上 `exp` 验证（PyJWT 默认验证 exp，但需要确保 token 确实包含 exp），并添加注释引导开发者补齐。

#### 4.2.3 缺少 Rate Limiting (🟡 中)

**建议**: 在架构文档中增加 `slowapi` 或自定义 middleware 的速率限制模式。

---

### 4.3 📊 可观测性 / Observability

#### 4.3.1 缺少 Metrics & Tracing (🔴 高)

**问题**: structlog 只覆盖了 Logging 部分。Metrics (Prometheus) 和 Distributed Tracing (OpenTelemetry) 完全缺失。

**竞品做法**: `fastapi-best-architecture` 内置 Grafana + Prometheus 集成。

**建议**:
1. 添加 `app/core/metrics.py` 模板（Prometheus `prometheus-fastapi-instrumentator`）
2. 在架构文档添加 Observability 章节，定义三大支柱: Logs + Metrics + Traces
3. 创建新 Skill: `add-observability`

#### 4.3.2 日志缺少标准库桥接 (🟡 中)

**问题**: skeleton 的 [logging.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/logging.py) 缺少架构文档 §4.7 中的标准库 `logging.basicConfig` 桥接。uvicorn、sqlalchemy 等第三方库日志不会经过 structlog 处理链。

**建议**: 将架构文档中完整的桥接代码同步到 skeleton。

---

### 4.4 🧪 测试 / Testing

#### 4.4.1 测试覆盖严重不足 (🔴 高)

**问题**: skeleton 只有 1 个 [test_health.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/tests/test_health.py)（4 行），无单元测试示例、无集成测试示例。[conftest.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/tests/conftest.py) 定义了 [postgres_engine](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/tests/conftest.py#19-24) fixture 但从未使用。`tests/domain/` 目录存在但为空。

**竞品做法**: 几乎所有竞品都提供完整的测试示例（含 CRUD 测试、认证测试等）。

**建议**:
1. 添加 `tests/unit/test_exceptions.py` — 验证异常体系
2. 添加 `tests/unit/test_auth.py` — 验证 JWT 依赖
3. 添加 `tests/integration/test_example_crud.py` — 演示 Testcontainers 集成测试
4. 在 [conftest.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/tests/conftest.py) 中提供 [db_session](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/dependencies.py#13-19) fixture（架构文档 §4.9 中已定义但 skeleton 缺失）

#### 4.4.2 CI 缺少 Coverage 报告 (🟡 中)

**建议**:
```yaml
# ci.yml 添加
- name: Pytest with coverage
  run: uv run pytest --cov=app --cov-report=xml --tb=short
```
```toml
# pyproject.toml 添加
[tool.coverage.run]
source = ["app"]
omit = ["*/migrations/*"]
```

---

### 4.5 📁 Skill 系统 / Agent Skills

#### 4.5.1 引用资源不存在 (🟡 中)

**问题**: 所有 6 个 Skill 的 SKILL.md 引用了不存在的路径:

| Skill | 引用的缺失资源 |
|---|---|
| `server-init` | `scripts/apply_skeleton.py`, `references/bootstrap-checklist.md` |
| `add-domain-module` | `scripts/scaffold_domain.py`, `references/domain-patterns.md` |
| `add-infra-adapter` | `scripts/scaffold_adapter.py`, `references/adapter-patterns.md` |
| `alembic-migration` | `references/migration-checklist.md` |
| `ci-setup` | `assets/ci.template.yml`, `references/ci-options.md` |
| `docker-deploy` | `assets/docker-compose.template.yml`, `references/deploy-checklist.md` |

**影响**: Agent 执行这些 Skill 时会失败，因为引用的脚本/模板不存在。

**建议**: 
- 优先实现 `scripts/apply_skeleton.py` 和 `scripts/scaffold_domain.py`（最常用）
- 将 `references/` 下的 checklist 文档补全
- 将 `assets/` 下的模板文件补全

#### 4.5.2 缺少常用 Skill (🟡 中)

建议新增：

| Skill 名 | 用途 |
|---|---|
| `add-background-task` | 集成 Celery / ARQ 后台任务 |
| `add-websocket` | WebSocket 模块脚手架 |
| `add-middleware` | 自定义中间件模板（Rate Limit, Request ID, CORS 增强等）|
| `add-observability` | Prometheus + OpenTelemetry 集成 |
| `convert-to-async` | 将同步模块转换为异步 |

---

### 4.6 🔧 工具链 / Tooling

#### 4.6.1 缺少 pre-commit hooks (🟡 中)

**竞品做法**: `one-zero-eight/fastapi-template` 内置 `.pre-commit-config.yaml`。

**建议**: 添加 `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/RobertCraiworthy/pyright-python
    rev: v1.1.400
    hooks:
      - id: pyright
```

#### 4.6.2 Dockerfile skeleton 与架构文档不一致 (🟡 中)

| 差异项 | 架构文档 ([docs/architecture.md](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/docs/architecture.md)) | Skeleton ([skeleton/Dockerfile](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/Dockerfile)) |
|---|---|---|
| Python 版本 | `3.13-slim` | `3.12-slim` |
| `uv.lock` 复制 | `COPY pyproject.toml uv.lock ./` | `COPY pyproject.toml ./` (缺 `uv.lock`) |
| `--frozen` flag | `uv sync --frozen --no-dev` | `uv sync --no-dev \|\| true`(容错但不确定性) |

**建议**: 统一为架构文档的版本，确保确定性构建。

#### 4.6.3 Makefile 缺少常用命令 (🟢 低)

与架构文档 §3 对比，skeleton Makefile 缺少:
- `test-unit` — 仅运行单元测试
- `migrate` — 数据库迁移
- `security` — 安全扫描 (建议新增)

---

### 4.7 📁 项目结构 / Project Structure

#### 4.7.1 缺少 docker-compose.yml (🟡 中)

**问题**: 本地开发需要 PostgreSQL + Redis，但 skeleton 无 `docker-compose.yml`。开发者需自行搭建。

**竞品做法**: 几乎所有竞品都内置 `docker-compose.yml`。

**建议**: 添加 `docker-compose.yml`:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: koi_service
      POSTGRES_PASSWORD: postgres
    ports: ["5432:5432"]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

#### 4.7.2 缺少项目元文件 (🟢 低)

- `CONTRIBUTING.md` — 贡献指南
- `CHANGELOG.md` — 版本变更日志
- `.dockerignore` — Docker 构建排除（skeleton 未包含）
- `.editorconfig` — 编辑器统一配置

---

### 4.8 🏗️ 架构文档 vs 代码一致性 / Doc-Code Drift

| # | 架构文档描述 | Skeleton 实际情况 | 状态 |
|---|---|---|---|
| 1 | [setup_logging()](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/logging.py#8-27) 含标准库桥接 (§4.7) | 缺少 `logging.basicConfig` 桥接 | ⚠️ 漂移 |
| 2 | [db_session](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/dependencies.py#13-19) fixture 使用 `join_transaction_mode` (§4.9) | [conftest.py](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/tests/conftest.py) 缺少此 fixture | ⚠️ 漂移 |
| 3 | [setup_logging()](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/core/logging.py#8-27) 在 [create_app()](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/main.py#21-55) 内调用 (§4.0) | 放在 [lifespan()](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/app/main.py#15-19) 中 | ⚠️ 微调 |
| 4 | Dockerfile 用 Python 3.13 (§6) | skeleton 用 Python 3.12 | ⚠️ 漂移 |
| 5 | 完整的 Repository + UoW 示例 (§4.5) | skeleton 中缺少完整示例 | ⚠️ 漂移 |
| 6 | [pyproject.toml](file:///Volumes/Workspace/SourceCode/mrkoi/koi_blueprint_python/skeleton/pyproject.toml) target-version `py313` (§7.5) | skeleton 用 `py312` | ⚠️ 漂移 |

---

## 5. 优先级行动计划 / Prioritized Action Plan

### Phase 1: 紧急修复 (1-2 天)

1. **同步架构文档与 skeleton 代码** — 消除 §4.8 中所有漂移项
2. **补全 Skill 引用资源** — 至少实现 `scripts/apply_skeleton.py` + `scripts/scaffold_domain.py`
3. **添加示范测试** — unit + integration 各至少 1 个完整示例
4. **修正 Dockerfile** — 统一 Python 版本、添加 `uv.lock`、使用 `--frozen`

### Phase 2: 核心增强 (3-5 天)

5. **添加 Generic CRUD Repository 基类** — 消除领域模块样板代码
6. **添加安全扫描** — Bandit + pip-audit + CI 集成
7. **添加 pre-commit hooks** — `.pre-commit-config.yaml`
8. **添加 docker-compose.yml** — 本地开发环境一键启动
9. **添加 `.dockerignore`** — 优化 Docker 构建上下文

### Phase 3: 进阶能力 (1-2 周)

10. **添加 async 完整路径** — examples 或 Skill
11. **添加 Observability** — Prometheus + OpenTelemetry 模板
12. **添加后台任务模式** — Celery / ARQ 模板
13. **扩展 Skill 库** — `add-background-task`, `add-websocket`, `add-observability`
14. **升级 Repository 接口到 Protocol** — 更 Pythonic

### Phase 4: 锦上添花 (持续)

15. **添加 Cookiecutter 或 copier 支持** — 参数化项目生成
16. **添加 API 版本管理模式** — v1/v2 共存策略
17. **添加 Rate Limiting 模板** — slowapi 集成
18. **添加 `CONTRIBUTING.md` + `CHANGELOG.md`**

---

## 6. 结论 / Conclusion

> [!IMPORTANT]
> **Koi Blueprint Python 在同类项目中定位独特** — 它是唯一一个面向 AI Agent 的 Python 服务端架构模板。架构文档质量高于所有竞品，技术栈选型(Astral 全家桶)领先。
>
> **主要差距在于"骨架的完整度"**:
> - Skeleton 代码未完全实现架构文档描述的所有模式
> - Skill 系统是最大差异化优势，但引用的脚本/模板全部缺失
> - 测试、安全、可观测性基础设施需要补齐
>
> **建议策略**: 先 Phase 1 消除文档-代码漂移，再 Phase 2 补齐核心缺失，确保 "architecture.md 中说的每一句话，skeleton 都有对应实现"。

*报告版本: 1.0*
