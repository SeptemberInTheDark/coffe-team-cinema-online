FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

COPY . /app

WORKDIR /app

RUN pip install -r requirements/dev.txt

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]
