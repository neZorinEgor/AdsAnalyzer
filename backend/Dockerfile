FROM python:3.12-slim

WORKDIR app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN apt-get update && apt-get install -y wget

RUN apt-get -y install curl

RUN apt-get install libgomp1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD wget --tries=1 http://localhost:8000/healthcheck || exit 1
