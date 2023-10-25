FROM python:3
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

# install dependencies
#RUN pip install --upgrade pip

#RUN  apk add --no-cache python3 py3-pip python3-dev postgresql-libs && \
#     apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev  libjpeg-turbo-dev zlib-dev
#
#RUN apk add g++

#RUN apk add py3-zmq

#RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxslt-dev zeromq-dev

#apt


COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
