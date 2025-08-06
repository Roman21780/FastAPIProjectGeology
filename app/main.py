from fastapi import FastAPI
from app.core.middleware import add_exception_handlers, LoggingMiddleware
from app.core.logging import logger
from app.api.v1.api import router as api_router
from app.core.config import settings

def create_app() -> FastAPI:
    """Factory function for creating the FastAPI application"""
    app = FastAPI(
        title="Licensing Management API",
        version="1.0.0",
        debug=settings.DEBUG,
        docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
        redoc_url="/redoc" if settings.DEBUG else None
    )

    # Подключение middleware
    app.add_middleware(LoggingMiddleware)
    add_exception_handlers(app)

    # Подключение роутеров (убрано дублирование)
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup_event():
        """Log application startup"""
        logger.info("Application started", extra={
            "version": app.version,
            "debug": app.debug
        })

    @app.on_event("shutdown")
    async def shutdown_event():
        """Log application shutdown"""
        logger.info("Application shutting down")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)