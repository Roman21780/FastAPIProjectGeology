from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from app.core.logging import logger


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(
        f"HTTP error: {exc.status_code} - {exc.detail}",
        extra={"path": request.url.path}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path}
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.critical(
        f"Unhandled exception: {str(exc)}",
        extra={"path": request.url.path},
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "ip": request.client.host
            }
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                f"Request failed: {str(exc)}",
                exc_info=True,
                extra={
                    "method": request.method,
                    "path": request.url.path
                }
            )
            raise

        logger.info(
            f"Request completed: {response.status_code}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code
            }
        )

        return response