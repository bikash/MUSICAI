FROM python:3.6-slim

COPY . /app
WORKDIR /app

CMD ["python","hello.py"]
