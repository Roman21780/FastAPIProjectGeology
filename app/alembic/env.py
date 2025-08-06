import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

# Критически важный блок - добавляем корень проекта в PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

# Только после добавления пути импортируем модули приложения
from app.core.database import Base
from app.models.reference import *
from app.core.config import settings

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_online():
    connectable = create_engine(settings.DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()