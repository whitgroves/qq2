# syntax=docker/dockerfile:1

FROM python:3.12.0-slim

# for slim/alpine: install git first & clear apt cache
RUN apt update \
    && apt install -y --no-install-recommends git \
    && apt purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# instance setup - init_db contains test data
WORKDIR /qq2
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m init_db

# run
CMD [ "flask", "run", "--host=0.0.0.0", "--port=3223" ]
EXPOSE 3223