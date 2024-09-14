FROM python

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install -r requirements/dev.txt

# CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]
CMD [ "python", "src\app.py" ]
