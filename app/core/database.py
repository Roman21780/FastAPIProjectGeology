from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Преобразуем URL в строку, если это необходимо
database_url = str(settings.DATABASE_URL)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=100,
    connect_args={
        "connect_timeout": 5,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()