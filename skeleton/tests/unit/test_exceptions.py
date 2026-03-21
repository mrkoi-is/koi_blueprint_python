"""单元测试: 异常体系 (AppError hierarchy)"""

from app.core.exceptions import (
    AppError,
    AuthenticationError,
    BusinessValidationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)


class TestAppError:
    def test_default_values(self) -> None:
        err = AppError("something went wrong")
        assert err.message == "something went wrong"
        assert err.code == 500
        assert err.status == 500
        assert err.details == {}
        assert err.headers == {}

    def test_custom_values(self) -> None:
        err = AppError(
            "custom",
            code=50001,
            status=500,
            details={"key": "value"},
            headers={"X-Custom": "yes"},
        )
        assert err.code == 50001
        assert err.status == 500
        assert err.details == {"key": "value"}
        assert err.headers == {"X-Custom": "yes"}

    def test_args_propagation(self) -> None:
        """确保 exc.args[0] == message，日志/Sentry 可正确读取"""
        err = AppError("test message")
        assert err.args[0] == "test message"


class TestNotFoundError:
    def test_defaults(self) -> None:
        err = NotFoundError()
        assert err.status == 404
        assert err.code == 404
        assert err.message == "Resource not found"

    def test_custom_message(self) -> None:
        err = NotFoundError("User 42 not found")
        assert err.message == "User 42 not found"

    def test_custom_business_code(self) -> None:
        """业务子码: 40401 = 用户不存在"""
        err = NotFoundError("User not found", code=40401)
        assert err.code == 40401
        assert err.status == 404


class TestConflictError:
    def test_defaults(self) -> None:
        err = ConflictError()
        assert err.status == 409
        assert err.code == 409


class TestAuthenticationError:
    def test_defaults(self) -> None:
        err = AuthenticationError()
        assert err.status == 401
        assert err.code == 401
        assert err.headers == {"WWW-Authenticate": "Bearer"}


class TestForbiddenError:
    def test_defaults(self) -> None:
        err = ForbiddenError()
        assert err.status == 403
        assert err.code == 403


class TestBusinessValidationError:
    def test_defaults(self) -> None:
        err = BusinessValidationError()
        assert err.status == 422
        assert err.code == 422

    def test_with_details(self) -> None:
        err = BusinessValidationError(details={"field": "name is required"})
        assert err.details == {"field": "name is required"}

    def test_custom_business_code(self) -> None:
        """业务子码: 42201 = 字段校验不通过"""
        err = BusinessValidationError("Invalid name", code=42201)
        assert err.code == 42201
        assert err.status == 422
