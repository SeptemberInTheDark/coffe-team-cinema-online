
FROM python

ENV PYTHONUNBUFFERED=1

RUN pip install virtualenv

WORKDIR /app

COPY requirements/dev.txt .

RUN pip install virtualenv && \
    virtualenv venv && \
    ./venv/bin/pip install -r dev.txt

COPY . .

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

