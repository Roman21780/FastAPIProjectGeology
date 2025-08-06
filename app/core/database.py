from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session  # Явно импортируем Session
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=20,       # Размер пула соединений
    max_overflow=100    # Максимальное количество соединений сверх pool_size
)

# SessionLocal - фабрика для создания сессий БД
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session  # Явно указываем класс сессии
)

Base = declarative_base()

# Генератор сессий для Dependency Injection
def get_db() -> Session:  # Явно указываем тип возвращаемого значения
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()