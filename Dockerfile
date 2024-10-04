
FROM python

ENV PYTHONUNBUFFERED=1

# Установите virtualenv
RUN pip install virtualenv

# Создайте рабочую директорию
WORKDIR /app

# Скопируйте файлы в контейнер
COPY requirements/dev.txt .

# Создайте виртуальное окружение
RUN virtualenv venv

# Установите зависимости в виртуальное окружение
RUN ./venv/bin/pip install -r dev.txt

# Скопируйте весь код приложения
COPY . .

# Укажите переменную окружения для использования виртуального окружения
ENV PATH="/app/venv/bin:$PATH"

# Откройте порт
EXPOSE 8000

# Запустите приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

