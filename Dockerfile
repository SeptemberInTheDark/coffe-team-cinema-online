
FROM python

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/dev.txt .

RUN pip install -r /requirements/dev.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
