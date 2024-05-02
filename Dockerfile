FROM python:3.11-alpine

COPY ./src /app/src

RUN pip install --no-cache-dir uvicorn fastapi Jinja2

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8001"]