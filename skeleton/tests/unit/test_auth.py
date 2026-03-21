"""单元测试: 认证与鉴权依赖 (auth.py)"""

import time

import jwt
import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.config import settings
from app.core.auth import get_current_user, get_optional_user, require_role
from app.core.exceptions import AuthenticationError, ForbiddenError


def _make_token(payload: dict) -> str:
    return jwt.encode(payload, settings.jwt_secret.get_secret_value(), algorithm="HS256")


def _make_credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


class TestGetCurrentUser:
    def test_missing_credentials_raises(self) -> None:
        with pytest.raises(AuthenticationError):
            get_current_user(None)

    def test_valid_token(self) -> None:
        token = _make_token({"sub": "123", "role": "admin"})
        creds = _make_credentials(token)
        user = get_current_user(creds)
        assert user["sub"] == "123"
        assert user["role"] == "admin"

    def test_invalid_token_raises(self) -> None:
        creds = _make_credentials("invalid.token.here")
        with pytest.raises(AuthenticationError):
            get_current_user(creds)

    def test_expired_token_raises(self) -> None:
        token = _make_token({"sub": "123", "exp": int(time.time()) - 3600})
        creds = _make_credentials(token)
        with pytest.raises(AuthenticationError):
            get_current_user(creds)


class TestGetOptionalUser:
    def test_no_credentials_returns_none(self) -> None:
        result = get_optional_user(None)
        assert result is None

    def test_valid_token_returns_payload(self) -> None:
        token = _make_token({"sub": "456"})
        creds = _make_credentials(token)
        result = get_optional_user(creds)
        assert result is not None
        assert result["sub"] == "456"

    def test_invalid_token_returns_none(self) -> None:
        creds = _make_credentials("bad.token")
        result = get_optional_user(creds)
        assert result is None


class TestRequireRole:
    def test_allowed_role(self) -> None:
        checker = require_role("admin", "editor")
        user = {"sub": "1", "role": "admin"}
        result = checker(user)
        assert result == user

    def test_disallowed_role_raises(self) -> None:
        checker = require_role("admin")
        user = {"sub": "1", "role": "viewer"}
        with pytest.raises(ForbiddenError):
            checker(user)

    def test_missing_role_raises(self) -> None:
        checker = require_role("admin")
        user = {"sub": "1"}
        with pytest.raises(ForbiddenError):
            checker(user)
