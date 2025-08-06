import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.core.config import settings

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(settings.LOG_FORMAT)

    logger = logging.getLogger("app")
    logger.setLevel(settings.LOG_LEVEL)

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файловый вывод с ротацией
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=settings.LOG_ROTATION_SIZE * 1024 * 1024,
        backupCount=settings.LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging()