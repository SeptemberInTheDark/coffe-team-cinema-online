#!/bin/sh
# Применяем миграции
alembic upgrade head

# Запускаем приложение
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
