FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

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

RUN pip install virtualenv

WORKDIR /app

COPY requirements.txt .

RUN virtualenv venv && \
    ./venv/bin/pip install -r requirements.txt

COPY . .

ENV PATH="/app/venv/bin:$PATH"

# Копируем entrypoint-скрипт и делаем его исполняемым
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
