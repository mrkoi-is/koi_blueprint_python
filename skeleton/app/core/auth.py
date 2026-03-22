from collections.abc import Callable
from typing import Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.core.exceptions import AuthenticationError, ForbiddenError

bearer_scheme = HTTPBearer(auto_error=False)
optional_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    if credentials is None:
        raise AuthenticationError()
    try:
        payload: dict[str, Any] = jwt.decode(  # type: ignore[reportUnknownMemberType]
            credentials.credentials,
            settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError(f"Invalid token: {exc}") from exc
    return payload


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
) -> dict[str, Any] | None:
    if credentials is None:
        return None
    try:
        payload: dict[str, Any] = jwt.decode(  # type: ignore[reportUnknownMemberType]
            credentials.credentials,
            settings.jwt_secret.get_secret_value(),
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError:
        return None
    return payload


def require_role(*roles: str) -> Callable[..., dict[str, Any]]:
    def checker(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        if user.get("role") not in roles:
            raise ForbiddenError("Insufficient permissions")
        return user

    return checker
