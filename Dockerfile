FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
#netcat module is needed to check for the existence of a second container on the network
RUN apt-get install netcat -y

RUN mkdir /my_app_dir
WORKDIR /my_app_dir
ADD requirements.txt /my_app_dir/
RUN  pip install -r requirements.txt
ADD . /my_app_dir/
