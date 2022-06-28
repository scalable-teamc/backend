# start from base
FROM python:3.8-buster

# copy our application code
ADD . /app
WORKDIR /app

RUN apt-get update 

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# expose port
EXPOSE 5000

# Run this command on start
CMD [ "python", "-d", "./controller.py" ]




# NOTES:

# erase_upload_run.sh 
# A file to run on local machine. It Erase previous container & images, and create & run new one

# ERASE_ALL_CONTAINER: docker container rm -f $(docker container ls -aq)
# ERASE_IMG: docker rmi flask-api-test
# BUILD: docker build -t flask-api-test .
# RUN: docker run flask-api-test
