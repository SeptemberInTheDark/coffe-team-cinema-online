FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

# Установка необходимых системных зависимостей для компиляции пакетов
RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev \
    build-base \
    rust \
    cargo \
    openssl-dev \
    make

# Установка virtualenv
RUN pip install virtualenv

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Создание виртуального окружения и установка зависимостей
RUN virtualenv venv && \
    ./venv/bin/pip install -r requirements.txt

# Копирование всего проекта в контейнер
COPY . .

# Добавление виртуального окружения в PATH
ENV PATH="/app/venv/bin:$PATH"

# Команда для запуска приложения
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 & \
    python -m celery -A app.utils.celery_schedule worker --loglevel=info & \
    python -m celery -A app.utils.celery_schedule.celery_app beat --loglevel=INFO"]