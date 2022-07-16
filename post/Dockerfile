FROM python:3.9-slim

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY __init__.py .
COPY controller.py .
COPY post_app.py .
COPY post_db.py .
COPY post_helper.py .
COPY requirements.txt .

RUN pip install -r requirements.txt