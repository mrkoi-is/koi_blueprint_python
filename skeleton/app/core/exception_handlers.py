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
            "path": str(request.url.path),
        },
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "Request validation failed",
            "details": exc.errors(),
            "path": str(request.url.path),
        },
    )
