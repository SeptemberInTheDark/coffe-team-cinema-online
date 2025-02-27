#!/bin/sh

# Выполняем миграции базы данных
alembic upgrade head

# Запускаем Uvicorn для API
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 &

# Запускаем Celery worker
python -m celery -A app.utils.utils_notification.celery_schedule worker --loglevel=info &

# Запускаем Celery beat
python -m celery -A app.utils.utils_notification.celery_schedule.celery_app beat --loglevel=INFO

# Ожидаем завершения всех процессов
wait
