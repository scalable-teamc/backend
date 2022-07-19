FROM python:3.9-slim

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./post/post_app.py .
COPY ./post/post_controller.py .
COPY ./post/post_db.py .
COPY ./post/post_helper.py .
COPY ./post/post_init.py .
COPY ./post/requirements.txt .

RUN pip install -r requirements.txt

# ENV FLASK_APP=post_app.py

# CMD [ "python", "post_app.py" ]