# Koi Python Server 通用架构 (Enterprise Template)
> 可复用到所有项目的 Python 服务端架构模板 / Reusable Enterprise Python Server Architecture Template

> **适用范围**：本文档默认覆盖**同步/异步 HTTP API 服务**（包括 REST、WebSocket 接入层）。Worker、Cron、AI 推理服务、数据管道等非 HTTP 服务可复用本文档的工具链（§2.1）、配置（§4.1）、日志（§4.7）等通用部分，其余按各类型服务另行扩展。

---

## 1. 架构演进目标 (2026+) / Architecture Goals

该模板旨在解决多项目并行开发时的痛点，达成以下目标：
1. **极致开发者体验 (DX)**：毫秒级工具链 (Astral)、编译期类型安全、热重载。
2. **依赖倒置，边界清晰**：业务逻辑（Service）与框架（FastAPI）、ORM（SQLAlchemy）、外部系统（Infra）保持**依赖倒置**——核心逻辑不依赖交付层实现细节，关键外部依赖可替换、可模拟、可测试。
3. **低配置集成测试 (Low-Config Testing)**：使用 Testcontainers 编程化管理测试环境，无需手工维护固定本地数据库实例。仍依赖 Docker 运行环境。
4. **统一规范**：所有项目共享同一套目录结构、错误处理、日志、认证、缓存模式，消除跨项目上下文切换成本。

---

## 2. 技术栈（2026 终极形态） / Tech Stack

### 2.1 核心工具链 (The Astral Ecosystem)

> 「级别」列含义见 §2.6 标准分级。

| 工具 | 级别 | 说明 |
|---|---|---|
| **uv** | 强制 | 统一包管理与虚拟环境管理，替代 pip/poetry。显著提升依赖解析与安装速度。 |
| **Ruff** | 强制 | 统一 lint / format / import-sort 工具链，替代 flake8/black/isort。 |
| **pyproject.toml** | 强制 | 作为 **Python 工具链与项目元数据中心** (依赖、工具链、构建策略)。`.env`/Docker/CI 等配置仍各司其职。 |
| **pyright** | 强制 | 严格类型检查，配合 `SQLAlchemy 2.0 Mapped` 实现全链路类型安全。IDE 支持完善，是 CI 类型检查基线。 |
| **ty** | 试点 | Astral 出品的 Rust 实现类型检查器，速度极快。目前仍处于试点期，**生产 CI 不作为默认基线**，适合开发环境尝鲜；待生态成熟后评估切换。 |

### 2.2 Web 框架选型决策 (Framework Decision)

**选定：FastAPI**

| 候选 | 级别 | 评估结论 |
|---|---|---|
| **FastAPI** ✅ | 强制 (新项目) | Pydantic 原生集成，与本方案 DTO/DI/异常体系天然契合；async-first 且自动生成 OpenAPI 文档；社区生态成熟，第三方库覆盖全面。 |
| Litestar | 试点 | 序列化性能更优 (msgspec)、企业功能内置，但生态规模和第三方集成少于 FastAPI，适合在性能敏感非核心项目中验证。 |
| Flask 3.x | 例外 | 轻量灵活，但 async 支持有限，且深度绑定 Marshmallow，无法自然过渡到 Pydantic。**仅限存量项目维护，新项目不选。** |

> **原则**：框架是"边缘端点 (Delivery Mechanism)"，业务逻辑不依赖具体框架。Router 层只处理 HTTP 关注点（参数解析、状态码、DTO 转换），Service 层是纯 Python。

### 2.3 同步/异步策略 (Sync vs Async)

| 场景 | 策略 | 说明 |
|---|---|---|
| **默认** | 同步 `def` | FastAPI 自动将 `def` 路由放入线程池执行，多个请求可并行处理。心智负担最低。 |
| **高并发 I/O** | 异步 `async def` | WebSocket、长轮询、大量并发外部 API 调用场景。**必须**搭配异步驱动 (`asyncpg`) 和 `AsyncSession`，否则性能反而更差。 |

> **准则**：不要在 `async def` 中调用阻塞操作（同步 ORM、`time.sleep` 等）。如果不确定，用 `def`。

### 2.4 应用层规范 (Application Standards)
| 层 | 推荐选型 | 级别 | 设计约束 |
|---|---|---|---|
| **配置 (Config)** | `pydantic-settings` v2 | 强制 | 全面替代 `os.environ`。启动时强制类型校验，支持 `.env`、`SecretStr`、`env_prefix` 命名空间。 |
| **Web 框架** | FastAPI | 强制 (新项目) | 仅作为 Delivery Mechanism，Service 层不 import FastAPI 任何模块。 |
| **数据验证** | `Pydantic v2` | 推荐 | **API 边界层**（Router 入参/出参）强制使用 Pydantic DTO。Service 内部调用可直接传基础类型或 dataclass，按复杂度自行决定，避免 DTO 泛滥。 |
| **ORM** | `SQLAlchemy 2.0` | 推荐 | 强制使用 `Mapped[T]` + `mapped_column()` 类型标注，告别动态 `db.Column` 风格。 |
| **数据库迁移** | `Alembic` (独立使用) | 推荐 | 直接使用 Alembic CLI + `env.py`，不依赖 Flask-Migrate 等框架封装。 |
| **认证 (Auth)** | `PyJWT` + FastAPI `Depends` | 推荐 | 以 `Depends` 为主实现认证与鉴权（`get_current_user` / `require_role`），中间件层可作为可选扩展（如全局请求日志注入用户上下文）。 |
| **缓存 (Cache)** | `redis` (async/sync) | 推荐 | 通过 `infra/` 适配器封装，Service 层通过抽象接口调用，不直接依赖 Redis SDK。 |
| **依赖注入 (DI)** | FastAPI `Depends` + 工厂函数 | 强制 | Service 层不自己创建 DB Session / Cache Client / HttpClient，全部由外部注入。 |

### 2.5 测试与日志基础 (Testing & Logging)

> Metrics / Distributed Tracing 等进阶可观测性能力按项目运维需求另行引入，不在本模板强制范围内。

| 组件 | 级别 | 说明 |
|---|---|---|
| **单元测试** | 推荐 | `pytest` + `pytest-mock`。纯业务逻辑测试，毫秒级执行。Service 依赖 MemoryRepository 替身。 |
| **集成测试** | 推荐 | `testcontainers`（需安装对应 extra，如 `testcontainers[postgres]`）。自动拉起临时容器，测完即焚，依赖 Docker 环境。 |
| **结构化日志** | 强制 | `structlog`。开发环境 ConsoleRenderer 人类可读，生产环境 JSONRenderer 机器可解析。通过 `contextvars` 自动绑定 `trace_id`。 |

### 2.6 标准分级 (Standards Classification)

所有技术选型按约束力分为四级，**新项目必须遵守强制标准**，其余按项目复杂度选用。

| 级别 | 含义 | 技术项 |
|---|---|---|
| **强制** | 所有项目必须遵守 | `uv`、`Ruff`、`pyproject.toml`、`pyright`、`pydantic-settings`、FastAPI (新项目)、`structlog`、App Factory、统一异常体系、领域化目录结构 |
| **推荐** | 默认采用，经审批可豁免 | `SQLAlchemy 2.0 Mapped`、Repository 模式、Unit of Work、Testcontainers、`ApiResponse` 统一包装、Pydantic DTO (API 边界层) |
| **试点** | 允许在非核心项目中验证 | `ty` 类型检查器、`Litestar` 框架 |
| **例外** | 仅限存量项目维护 | Flask 3.x + Marshmallow、旧式 `db.Column` ORM |

> **豁免规则**：推荐标准的豁免需在项目 README 中注明理由（如"纯 CRUD 管理后台，跳过 UoW"）。

### 2.7 Python 版本治理策略 (Python Version Policy)

独立维护版本策略，避免每次 Python 小版本升级都修改主架构文档。模板示例中出现的具体版本号（如 `3.13`）均以本表策略为准。

| 策略项 | 当前值 | 说明 |
|---|---|---|
| **组织基线版本** | Python 3.12+ | 所有在维项目的最低运行版本要求，低于此版本不再提供支持 |
| **新项目优先版本** | Python 3.13 | 新建项目使用的推荐版本，与当前 CPython 稳定版保持一致 |
| **兼容窗口** | 当前稳定版 ± 1 | 同时支持前一个和当前稳定大版本，确保升级过渡期存量项目正常运行 |
| **升级节奏** | 每年 Q1 评估 | 随 CPython 年度发布节奏，每年第一季度评估是否将新版本设为优先版本 |

> 当 CPython 发布新稳定版后，由架构组评估后更新本表，无需修改其他章节。

---

## 3. 标准目录结构 (Universal Directory Structure)

推行"根据业务领域打包 (Package by Feature/Domain)"的结构，而非传统的"按技术层打包"。

```text
{project}/
├── pyproject.toml            ← Python 工具链与项目元数据中心
├── uv.lock                   ← 由 uv 维护，确保依赖确定性
├── Dockerfile                ← 标准的多阶段构建镜像
├── Makefile                  ← 统一开发者命令入口
├── .github/workflows/ci.yml  ← Lint → Type Check → Unit Test → Build
│
├── app/
│   ├── main.py               ← App 工厂 (create_app)，组装路由、中间件、异常处理器、生命周期
│   ├── config.py             ← 基于 Pydantic Settings 的强类型配置类
│   │
│   ├── core/                 ← 【跨项目可复用资产 / Reusable Core Assets】
│   │   ├── exceptions.py     ── 统一业务异常层次 (AppError → NotFoundError, ConflictError...)
│   │   ├── exception_handlers.py ── 全局异常处理器，AppError → 标准 JSON 响应
│   │   ├── responses.py      ── 标准 API 响应 DTO (ApiResponse[T])
│   │   ├── logging.py        ── structlog 初始化，dev/prod 双模式输出
│   │   ├── auth.py           ── JWT 验签、get_current_user 依赖提取器
│   │   ├── dependencies.py   ── 通用 DI 提取器 (get_db_session, get_redis)
│   │   ├── uow.py            ── Unit of Work 抽象接口
│   │   └── pagination.py     ── 分页参数与分页响应 DTO
│   │
│   ├── domain/               ← 【业务生命周期模块 / Business Domains】
│   │   ├── {module_a}/       ── 例如: auth, device, store
│   │   │   ├── router.py     ── 【只处理】参数解析 → 调用 Service → 返回 DTO
│   │   │   ├── schemas.py    ── Pydantic DTOs (请求与响应模型)
│   │   │   ├── models.py     ── SQLAlchemy 2.0 Mapped ORM
│   │   │   ├── service.py    ── 纯 Python 业务逻辑（类），不依赖 Web 框架
│   │   │   ├── repository.py ── 抽象接口 (AbstractXxxRepository)
│   │   │   ├── repository_sa.py ── SQLAlchemy 2.0 实现 (select + scalars)
│   │   │   └── uow.py        ── 领域级 UoW，挂载本领域 Repository
│   │   └── {module_b}/
│   │
│   └── infra/                ← 【外部适配器 / Adapters】
│       ├── cache.py          ── Redis 缓存抽象接口与实现
│       ├── qiniu_client.py   ── 对象存储适配器
│       └── mqtt_client.py    ── MQTT 消息适配器
│
├── alembic.ini               ← Alembic 配置文件 (项目根目录)
├── migrations/               ← Alembic 版本控制历史 (独立使用，不依赖 Flask-Migrate)
│   ├── env.py
│   └── versions/
│
└── tests/
    ├── conftest.py           ── Testcontainers 启动脚本与 Session/Function Fixtures
    ├── unit/                 ── Service 和 Core 测试，使用 MemoryRepository
    └── integration/          ── API 测试，连接 Testcontainers 临时数据库
```

### Makefile 标准命令

```makefile
.DEFAULT_GOAL := help

dev:       ## 启动开发服务器
	uv run uvicorn app.main:app --reload

test:      ## 运行全部测试
	uv run pytest

test-unit: ## 仅运行单元测试
	uv run pytest tests/unit

lint:      ## 代码检查并自动修复
	uv run ruff check . --fix

format:    ## 代码格式化
	uv run ruff format .

typecheck: ## 类型检查
	uv run pyright

migrate:   ## 执行数据库迁移
	uv run alembic upgrade head

help:      ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
```

---

## 4. 关键架构模式 (Key Architectural Patterns)

### 4.0 App 工厂与生命周期 (Application Factory & Lifespan)

所有模块在此组装。使用 FastAPI **Lifespan** 管理数据库连接池、Redis 等资源的启动与销毁。

```python
# app/main.py
import uuid
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import AppError
from app.core.exception_handlers import app_error_handler, validation_error_handler
from app.domain.device.router import router as device_router
from app.domain.store.router import router as store_router
# ... 其他 domain routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup：此处仅管理需要异步初始化的长连接资源
    # engine = create_engine(str(settings.database_url), pool_size=5, max_overflow=10)
    # redis_client = redis.from_url(settings.redis_url)
    yield
    # Shutdown
    # engine.dispose()
    # redis_client.close()


def create_app() -> FastAPI:
    # 日志在进程启动时立即初始化，早于任何模块级日志调用
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- 全局异常处理（业务异常 + Pydantic 参数校验统一为同一 JSON 格式）---
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    # --- 请求日志中间件 ---
    @app.middleware("http")
    async def logging_middleware(request, call_next):
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            trace_id=str(uuid.uuid4()),
            method=request.method,
            path=str(request.url.path),
        )
        response = await call_next(request)
        return response

    # --- 路由注册 ---
    api_prefix = "/api/v1"
    app.include_router(device_router, prefix=api_prefix)
    app.include_router(store_router, prefix=api_prefix)
    # ... 其他 domain routers

    # --- 健康检查 ---
    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
```

### 4.1 强类型配置 (Pydantic Settings)

替代散落各处的 `os.getenv`，在启动时即刻暴露环境变量错误。

```python
# app/config.py
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",             # Docker/K8s 中 .env 可能不存在，
        env_file_encoding="utf-8",   # pydantic-settings 会自动回退读取 OS 环境变量，可忽略文件缺失警告
        env_prefix="APP_",           # 所有变量加 APP_ 前缀，避免命名冲突
    )

    app_name: str = "Koi Server"
    debug: bool = False
    database_url: PostgresDsn
    jwt_secret: SecretStr  # 敏感字段，repr 时自动遮蔽
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: list[str] = ["http://localhost:3000"]  # 生产环境设为实际域名列表

settings = Settings()
# 如果 .env 缺少 APP_DATABASE_URL 或 APP_JWT_SECRET，程序直接崩溃退出
```

### 4.2 统一异常体系 (Exception Hierarchy)

所有业务异常继承 `AppError`，框架层通过全局处理器统一转换为标准 JSON 响应。

```python
# app/core/exceptions.py
class AppError(Exception):
    """所有业务异常的基类"""
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status: int = 500,
        details: dict | None = None,
        headers: dict[str, str] | None = None,
    ):
****        super().__init__(message)  # 确保 exc.args[0] == message，日志/Sentry 可正确读取
        self.message = message
        self.code = code
        self.status = status
        self.details = details or {}
        self.headers = headers

class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="NOT_FOUND", status=404)

class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, code="CONFLICT", status=409)

class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message, code="UNAUTHORIZED", status=401,
                         headers={"WWW-Authenticate": "Bearer"})

class ForbiddenError(AppError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, code="FORBIDDEN", status=403)

class BusinessValidationError(AppError):
    """业务校验错误（与 Pydantic 的 ValidationError 区分）"""
    def __init__(self, message: str = "Validation failed", details: dict | None = None):
        super().__init__(message, code="BUSINESS_VALIDATION_ERROR", status=422, details=details)
```

```python
# app/core/exception_handlers.py
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.exceptions import AppError

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        headers=exc.headers,
        content={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
            "path": str(request.url),
        },
    )

async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """将 Pydantic 参数校验错误统一为与 AppError 相同的 JSON 格式"""
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": exc.errors(),
            "path": str(request.url),
        },
    )

# 注册方式见 §4.0 create_app
```

### 4.3 标准 API 响应 (ApiResponse DTO)

```python
# app/core/responses.py
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: T | None = None

class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
```

> **豁免场景**：以下场景**不应**使用 `ApiResponse` 包装，直接返回原始响应：
> - 文件下载（`FileResponse` / `StreamingResponse`）
> - 流式响应 / SSE（`EventSourceResponse`）
> - WebSocket 消息帧
> - 204 No Content（空响应）
> - Webhook 回调（格式由对方平台约定）
> - `/health` 健康检查（格式由基础设施约定）

```python
# app/core/pagination.py
from fastapi import Query

class PaginationParams:
    """分页参数依赖 — 通过 Depends() 注入 Router"""
    def __init__(
        self,
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(20, ge=1, le=100, description="每页条数"),
    ):
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size
```

### 4.4 认证与鉴权 (Authentication)

采用 FastAPI 原生 `Depends` 机制，将 JWT 验签封装为可注入依赖。

> **适用范围**：本节为**内建认证基线**，适合内部管理后台、中小型业务 API、统一认证网关下游服务。对于对外开放 API、多租户平台、第三方 SSO / OIDC / OAuth2 Provider 对接场景，可在此基线之上升级为外部身份提供商模式（出 scope，需另行规划）。

```python
# app/core/auth.py
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """解码 JWT，返回 payload。验证失败抛出 AuthenticationError。"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
        )
        return payload
    except jwt.InvalidTokenError as e:
        raise AuthenticationError(f"Invalid token: {e}")

def require_role(*roles: str):
    """角色检查依赖工厂"""
    def checker(user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") not in roles:
            raise ForbiddenError("Insufficient permissions")
        return user
    return checker

def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> dict | None:
    """可选认证 — 公开接口中如果携带 Token 则解析，否则返回 None"""
    if credentials is None:
        return None
    try:
        return jwt.decode(
            credentials.credentials,
            settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError:
        return None
```

```python
# 使用示例 — 在 router.py 中
@router.get("/admin/dashboard")
def admin_dashboard(user: dict = Depends(require_role("admin"))):
    return {"message": f"Welcome, {user['username']}"}

@router.get("/public/feed")
def public_feed(user: dict | None = Depends(get_optional_user)):
    """公开接口：未登录可访问，登录后可个性化"""
    return {"personalized": user is not None}
```

> **生产环境 JWT 检查清单**：上述为最小模板示例，生产环境还需补齐：过期时间 (`exp`)、签发者/受众 (`iss`/`aud`)、刷新令牌 (Refresh Token) 机制、令牌黑名单/登出、密钥轮换策略、密码哈希 (`argon2`/`bcrypt`)。

### 4.5 Repository & Unit of Work (解耦数据库)

**痛点**：Service 里面全是 `db.session.commit()`，无法对业务逻辑进行单测。
**方案**：仓储模式 (操作单个聚合根) + 工作单元 (控制整体事务)。

> **适用性说明**：Repository + UoW 为**推荐标准**，适合有复杂事务边界、多外部依赖、需要高可测性的业务域。对于纯 CRUD 管理后台或生命周期简单的小型服务，可跳过 UoW，直接在 Service 中注入 Session 操作数据库（需在项目 README 注明豁免理由，参见 §2.6）。

```python
# app/core/uow.py
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class AbstractUnitOfWork(ABC):
    """工作单元抽象 — 每个项目按需声明所包含的 Repository 属性"""

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.rollback()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy 实现 — 项目级子类负责挂载具体 Repository"""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session: Session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
```

```python
# app/domain/device/repository.py — 抽象接口
from abc import ABC, abstractmethod

class AbstractDeviceRepository(ABC):
    @abstractmethod
    def get_by_sn(self, sn: str) -> Device | None: ...

    @abstractmethod
    def add(self, device: Device) -> None: ...

    @abstractmethod
    def list_all(self, offset: int = 0, limit: int = 20, **filters) -> list[Device]: ...

    @abstractmethod
    def count(self, **filters) -> int: ...
```

```python
# app/domain/device/repository_sa.py — SQLAlchemy 2.0 实现
from sqlalchemy import select, func
from sqlalchemy.orm import Session

class SaDeviceRepository(AbstractDeviceRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_sn(self, sn: str) -> Device | None:
        stmt = select(Device).where(Device.sn == sn)
        return self._session.scalar(stmt)

    def add(self, device: Device) -> None:
        self._session.add(device)

    def list_all(self, offset: int = 0, limit: int = 20, **filters) -> list[Device]:
        stmt = select(Device)
        if store_id := filters.get("store_id"):
            stmt = stmt.where(Device.store_id == store_id)
        stmt = stmt.offset(offset).limit(limit)
        return list(self._session.scalars(stmt))

    def count(self, **filters) -> int:
        stmt = select(func.count()).select_from(Device)
        if store_id := filters.get("store_id"):
            stmt = stmt.where(Device.store_id == store_id)
        return self._session.scalar(stmt) or 0
```

```python
# app/domain/device/uow.py — 项目级 UoW，挂载本领域的 Repository
class DeviceUnitOfWork(SqlAlchemyUnitOfWork):
    devices: AbstractDeviceRepository

    def __enter__(self) -> "DeviceUnitOfWork":
        super().__enter__()
        self.devices = SaDeviceRepository(self._session)
        return self
```

```python
# app/domain/device/service.py — 纯 Python 业务逻辑（类）
# 不知道 SQLAlchemy / FastAPI / Redis 的存在，只知道 UoW 和 Repository 接口

class DeviceService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    def register(self, sn: str) -> Device:
        with self._uow:
            if self._uow.devices.get_by_sn(sn):
                raise ConflictError("Device already exists")
            device = Device(sn=sn)
            self._uow.devices.add(device)
            self._uow.commit()
            return device

    def list(self, offset: int, limit: int) -> tuple[list[Device], int]:
        with self._uow:
            items = self._uow.devices.list_all(offset=offset, limit=limit)
            total = self._uow.devices.count()
            return items, total
```

### 4.6 显式依赖注入 (Explicit Dependency Injection)

Router 层通过 FastAPI `Depends` 注入已配好依赖的 Service 实例。

```python
# app/core/dependencies.py
from collections.abc import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db_session() -> Generator[Session, None, None]:
    """简单读操作可直接注入 Session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_device_uow() -> DeviceUnitOfWork:
    """写操作通过 UoW 管理事务与 Repository"""
    return DeviceUnitOfWork(SessionLocal)

def get_device_service(uow: DeviceUnitOfWork = Depends(get_device_uow)) -> DeviceService:
    return DeviceService(uow)
```

```python
# app/domain/device/router.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_device_service
from app.core.responses import ApiResponse, PaginatedData
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/devices", tags=["devices"])

@router.post("/", status_code=201, response_model=ApiResponse[DeviceSchema])
def create_device(
    payload: DeviceCreateSchema,
    service: DeviceService = Depends(get_device_service),
):
    device = service.register(payload.sn)
    return ApiResponse(data=device)

@router.get("/", response_model=ApiResponse[PaginatedData[DeviceSchema]])
def list_devices(
    pagination: PaginationParams = Depends(),
    service: DeviceService = Depends(get_device_service),
):
    items, total = service.list(pagination.offset, pagination.page_size)
    return ApiResponse(data=PaginatedData(
        items=items, total=total,
        page=pagination.page, page_size=pagination.page_size,
    ))
```

### 4.7 结构化日志 (Structured Logging)

开发环境输出人类可读格式，生产环境输出 JSON，通过 `contextvars` 自动绑定请求级上下文。

```python
# app/core/logging.py
import logging
import structlog
from app.config import settings

def setup_logging() -> None:
    shared_processors = [
        structlog.contextvars.merge_contextvars,  # 自动注入 trace_id, user_id 等
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if settings.debug:
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # 桥接标准库 logging：第三方库（uvicorn、sqlalchemy 等）通过
    # logging.getLogger() 输出的日志也会流经 structlog 处理链，
    # 确保整个进程日志格式统一。
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[structlog.stdlib.ProcessorFormatter.wrap_for_formatter(
            structlog.stdlib.ProcessorFormatter(
                processor=renderer,
                foreign_pre_chain=shared_processors,
            )
        )],
    )
```

> 日志中间件已整合到 §4.0 `create_app` 工厂中，不再需要单独声明。

### 4.8 缓存层 (Cache Abstraction)

通过抽象接口封装缓存操作，Service 层不直接依赖 Redis SDK。

```python
# app/infra/cache.py
from abc import ABC, abstractmethod
from typing import Any
import json
import redis

class AbstractCache(ABC):
    @abstractmethod
    def get(self, key: str) -> Any | None: ...

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 300) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...


class RedisCache(AbstractCache):
    def __init__(self, client: redis.Redis) -> None:
        self._client = client

    def get(self, key: str) -> Any | None:
        raw = self._client.get(key)
        return json.loads(raw) if raw else None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        self._client.setex(key, ttl, json.dumps(value))

    def delete(self, key: str) -> None:
        self._client.delete(key)


class MemoryCache(AbstractCache):
    """用于单元测试的内存替身"""
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        return self._store.get(key)

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        self._store[key] = value

    def delete(self, key: str) -> None:
        self._store.pop(key, None)
```

### 4.9 编程化集成测试 (Testcontainers)

只要有 Docker，`pytest` 随时随地运行。Session 级容器 + Function 级会话，平衡速度与隔离性。

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_engine():
    """Session 级：整个测试周期只启动一次 PG 容器"""
    with PostgresContainer("postgres:16-alpine") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
    # 测试结束，容器自动销毁

@pytest.fixture(scope="function")
def db_session(postgres_engine):
    """Function 级：每个测试用例获得独立的事务，测试结束自动回滚

    SQLAlchemy 2.0 写法：
      - `sessionmaker(bind=connection)` 已废弃并在 2.0 中移除
      - 改为 Session(connection, join_transaction_mode="create_savepoint")
      - join_transaction_mode 确保 session 加入外部事务而非自动提交
    """
    connection = postgres_engine.connect()
    transaction = connection.begin()
    session = Session(connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()
```

---

## 5. SQLAlchemy 2.0 模型规范

强制使用 `Mapped` 类型标注，确保全链路类型安全。

```python
# app/domain/device/models.py
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

class Device(TimestampMixin, Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sn: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(16), default="offline")
    store_id: Mapped[int | None] = mapped_column(ForeignKey("stores.id"))

    store: Mapped["Store | None"] = relationship(back_populates="devices")
```

---

## 6. Dockerfile 标准模板 (Multi-Stage Build)

使用 uv 的多阶段构建，确保生产镜像精简且构建速度快。

```dockerfile
# ---- Stage 1: Build ----
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

# ---- Stage 2: Runtime ----
FROM python:3.13-slim AS runtime

WORKDIR /app
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 7. 项目初始化向导 (Bootstrap Checklist)

当你需要创建一个新的通用后端项目时，执行以下命令：

### 7.1 构建基础工具链
```bash
uv init --python 3.13 my_project
cd my_project
uv add fastapi uvicorn[standard]
uv add pydantic pydantic-settings
uv add sqlalchemy psycopg[binary] alembic
uv add structlog pyjwt redis
```

### 7.2 构建开发环境
```bash
uv add --group dev ruff pyright pytest pytest-mock testcontainers[postgres]
# 若使用其他数据库，替换对应 extra，如 testcontainers[mysql]、testcontainers[mongodb]
# extra 列表见：https://testcontainers-python.readthedocs.io/en/latest/
```

### 7.3 初始化 Alembic
```bash
uv run alembic init migrations
# 编辑 migrations/env.py，导入项目的 Base.metadata
```

### 7.4 注入脚手架规范
- 复制上述的 `app/core/` 目录
- 复制 `Makefile`
- 配置 `pyproject.toml` 中的 `[tool.ruff]` 和 `[tool.pyright]`

### 7.5 pyproject.toml 工具配置参考
```toml
[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]

[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "strict"
```

### 7.6 验证与提交
```bash
make lint
make typecheck
make test
```

---

## 8. 架构约束清单 (Architecture Constraints Checklist)

在 Code Review 中强制执行的规则：

| # | 规则 | 违反示例 |
|---|---|---|
| 1 | **Router 不含业务逻辑** | Router 中出现 `if/else` 业务判断、直接操作 `db.session` |
| 2 | **Service 不依赖框架** | Service 中 `import fastapi` 或 `from flask import request` |
| 3 | **Service 不直接操作数据库** ¹ | Service 中出现 `session.query()`、`session.commit()` |
| 4 | **Model 使用 Mapped 类型** | 使用旧式 `db.Column(db.String)` 而非 `Mapped[str]` |
| 5 | **配置通过 Settings 读取** | 代码中出现 `os.getenv("XXX")` |
| 6 | **异常使用 AppError 体系** | 直接 `raise HTTPException(400, ...)` 而非 `raise BusinessValidationError(...)` |
| 7 | **外部依赖通过 infra/ 封装** | Service 中直接 `import qiniu` 或 `import paho.mqtt` |

> ¹ **豁免说明**：经 §2.6 豁免备案的纯 CRUD 轻量项目，允许 Service 通过注入 Session 直接操作数据库（跳过 UoW）。豁免须在项目 README 注明，并经架构负责人确认。

---

## 9. 不在本方案范围内 (Out of Scope)

以下内容需另行规划：

| 主题 | 说明 |
|---|---|
| **各项目落地计划** | 方案确定后，根据各项目现状制定分阶段迁移计划 |
| **CI/CD 流水线详设** | GitHub Actions / GitLab CI 的具体 YAML 配置 |
| **容器编排与部署** | Kubernetes / Docker Compose 生产部署策略 |
| **API 版本管理** | `/v1` → `/v2` 路由共存与废弃策略 |
| **性能基准** | 当前架构 vs 新架构的 QPS / 延迟对比测试 |
| **数据库迁移兼容** | 新旧 ORM 风格共存期间的 Alembic 迁移脚本策略 |

---

*文档版本：3.4 (2026/03) - Enterprise Arch Edition*
