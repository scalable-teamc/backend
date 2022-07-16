FROM python:3.9-slim

WORKDIR /profile/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./profile_service/__init__.py .
COPY ./profile_service/profile.py .
COPY ./profile_service/profile_account.py .
COPY ./profile_service/profile_app.py .
COPY ./profile_service/profile_controller.py .
COPY ./profile_service/requirements.txt .

RUN pip install -r requirements.txt

CMD [ "flask", "run", "profile_app.py" ]