FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

RUN pip install -r app/requirements/dev.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
