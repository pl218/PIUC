FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /PIUC
WORKDIR /PIUC
ADD requirements.txt /PIUC/
RUN pip install -r requirements.txt
ADD . /PIUC/