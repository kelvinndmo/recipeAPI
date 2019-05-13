FROM python:3.7-alpine
MAINTAINER Kelvin Onkundi Ndemo

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
#use package manager and add a package and no-cache means don't store the 
#registry index on our docker file to minimize extra files and packages 
#included in our docker container meaning no extra dependencies that may creat
#security vulnerabilities
RUN apk add --update --no-cache postgresql-client

#setup an alias for our depenciies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
