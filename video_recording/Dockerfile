FROM python:3.12.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y \
    ffmpeg \
    fonts-dejavu-core \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./main.py /app/main.py

