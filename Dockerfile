FROM python:3.8.12-slim

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

CMD ["sh", "-c", "./startup.sh ${PORT}"]
