FROM python:3.9-slim

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./feed_service/__init__.py .
COPY ./feed_service/feed.py .
COPY ./feed_service/feed_controller.py .
COPY ./feed_service/feed_db.py .
COPY ./feed_service/requirements.txt .

RUN pip install -r requirements.txt