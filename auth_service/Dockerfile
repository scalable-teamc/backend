FROM python:3.9-slim

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src"


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./auth_service/auth_app.py ./auth_service
COPY ./auth_service/__init__.py ./auth_service
COPY ./auth_service/auth_controller.py ./auth_service
COPY ./auth_service/auth_svc.py ./auth_service
COPY ./auth_service/user_account.py ./auth_service
COPY ./auth_service/requirements.txt .

RUN pip install -r requirements.txt


# ENV FLASK_APP=auth_app.py

# CMD [ "python", "auth_app.py"]
