# syntax=docker/dockerfile:1

FROM python:3.12.0-slim

# for slim/alpine: install git then clear apt cache
RUN apt update \
    && apt install -y --no-install-recommends git \
    && apt purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# instance setup - app will create its own db
WORKDIR /qq2
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# run
CMD export $(cat .env) && flask run --host=0.0.0.0 --port=80
EXPOSE 80