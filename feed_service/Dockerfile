FROM python:3.9-slim

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY __init__.py .
COPY feed.py .
COPY feed_controller.py .
COPY feed_db.py .
COPY requirements.txt .

RUN pip install -r requirements.txt