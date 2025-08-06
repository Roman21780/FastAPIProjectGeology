# Licensing Management API

REST API для управления лицензиями, месторождениями и скважинами в нефтегазовой отрасли.

## Технологии
- Python 3.9+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Docker

## Установка и запуск

### 1. Требования
- Docker 20.10+
- docker-compose 1.29+

### 2. Запуск в Docker
```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/licensing-management.git
cd licensing-management

# Создать .env файл (скопировать из примера)
cp .env.example .env

# Запустить сервисы
docker-compose up -d --build

# Применить миграции
docker-compose exec web alembic upgrade head
________________________________________________________

### 3. Приложение будет доступно по адресу: http://localhost:8000

## Доступные эндпоинты

Документация API: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

# Запуск тестов

docker-compose exec web pytest

# Инициализация alembic
alembic init alembic

# Создать новую миграцию
alembic revision --autogenerate -m "Добавлена таблица компаний"
docker-compose exec web alembic revision --autogenerate -m "description"

# Применить миграции
alembic upgrade head
docker-compose exec web alembic upgrade head

# Остановка приложения
docker-compose down

# Генерация секретного ключа
openssl rand -hex 32