from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from app.core.middleware import add_exception_handlers, LoggingMiddleware
from app.core.logging import logger
from app.api.v1.api import router as api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan handler for startup and shutdown events"""
    # Startup logic
    logger.info(
        "Application starting",
        extra={"version": "1.0.0", "debug": settings.DEBUG}
    )

    yield

    # Shutdown logic
    logger.info("Application shutting down")


def create_app() -> FastAPI:
    """Factory function for creating the FastAPI application"""
    fastapi_app = FastAPI(
        title="Licensing Management API",
        version="1.0.0",
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )

    # Подключение middleware
    fastapi_app.add_middleware(LoggingMiddleware)  # type: ignore[arg-type]
    add_exception_handlers(fastapi_app)

    # Подключение роутеров
    fastapi_app.include_router(api_router, prefix="/api/v1")

    return fastapi_app


app_instance = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app_instance",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )