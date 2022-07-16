FROM python:3.9-slim

WORKDIR /post/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./post/__init__.py .
COPY ./post/post_controller.py .
COPY ./post/post_app.py .
COPY ./post/post_db.py .
COPY ./post/post_helper.py .
COPY ./post/requirements.txt .

RUN pip install -r requirements.txt

CMD [ "flask", "run", "post_app.py" ]