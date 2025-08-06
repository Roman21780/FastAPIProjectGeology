import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
from app.core.config import settings


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Логгер для приложения
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый обработчик с ротацией
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Логгер для SQLAlchemy
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.INFO)

    # Логгер для запросов
    request_logger = logging.getLogger('request')
    request_handler = RotatingFileHandler(
        log_dir / "request.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    request_handler.setFormatter(formatter)
    request_logger.addHandler(request_handler)

    return logger


logger = setup_logging()