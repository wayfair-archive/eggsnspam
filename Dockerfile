FROM ubuntu:latest
MAINTAINER Jonathan Biddle "jbiddle@wayfair.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential freetds-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
