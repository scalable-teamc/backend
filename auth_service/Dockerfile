FROM python:3.9-slim

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY auth_app.py .
COPY __init__.py .
COPY auth_controller.py .
COPY auth_svc.py .
COPY user_account.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
