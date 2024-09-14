FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install -r requirements/dev.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
