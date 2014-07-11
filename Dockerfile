FROM debian:latest

MAINTAINER Zlatozar Zhelyazkov <zlatozar@gmail.com>

RUN apt-get update

RUN apt-get install -y git
RUN apt-get install -y python-pip
RUN apt-get install -y python2.7-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
