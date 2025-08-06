from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Настройки приложения
    DEBUG: bool = Field(True)
    APP_TITLE: str = Field("Licensing Management API")
    APP_VERSION: str = Field("1.0.0")
    API_PREFIX: str = Field("/api/v1")

    # Настройки базы данных
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("Serebro11!!")
    POSTGRES_DB: str = Field("licensing_db")
    DATABASE_URL: str = Field(
        default="postgresql://postgres:Serebro11!!@localhost:5432/licensing_db",
        description="URL подключения к БД"
    )

    # Настройки логирования
    LOG_LEVEL: str = Field("INFO")
    LOG_FORMAT: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_ROTATION_SIZE: int = Field(10)  # MB
    LOG_BACKUP_COUNT: int = Field(5)

    # Настройки экспорта
    MAX_EXPORT_ROWS: int = Field(10000)
    EXPORT_FORMATS: List[str] = ["csv", "xlsx"]

    # Безопасность
    SECRET_KEY: str = Field(os.getenv("SECRET_KEY"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(1440)  # 24 часа

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()