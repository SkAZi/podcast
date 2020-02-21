FROM python:alpine

ADD code /root/code
WORKDIR /root/code

RUN pip install -r requirements.txt