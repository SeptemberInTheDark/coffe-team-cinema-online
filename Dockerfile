FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

COPY . /app

WORKDIR /app

RUN pip install -r requirements/dev.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

