from typing import Any


class AppError(Exception):
    """统一业务异常基类。

    code 规则:
    - 默认值 = HTTP 状态码（如 404、500）
    - 业务细分 = HTTP 状态码 × 100 + 序号（如 40401 = 用户不存在、40402 = 订单不存在）
    """

    def __init__(
        self,
        message: str,
        code: int = 500,
        status: int = 500,
        details: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.details: dict[str, Any] = details or {}
        self.headers: dict[str, str] = headers or {}


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found", code: int = 404) -> None:
        super().__init__(message=message, code=code, status=404)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists", code: int = 409) -> None:
        super().__init__(message=message, code=code, status=409)


class AuthenticationError(AppError):
    def __init__(self, message: str = "Authentication required", code: int = 401) -> None:
        super().__init__(
            message=message,
            code=code,
            status=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenError(AppError):
    def __init__(self, message: str = "Permission denied", code: int = 403) -> None:
        super().__init__(message=message, code=code, status=403)


class BusinessValidationError(AppError):
    def __init__(
        self,
        message: str = "Validation failed",
        code: int = 422,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message=message, code=code, status=422, details=details)
