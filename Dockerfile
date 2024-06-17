FROM python:3.11-alpine

COPY ./.env /app/.env
COPY ./requirements.txt /app/requirements.txt
COPY ./www_requef /app/www_requef

WORKDIR /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "www_requef.main:app", "--host=0.0.0.0", "--port=8000"]
