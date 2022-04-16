FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /cinematica
WORKDIR /cinematica
COPY . /cinematica/
RUN pip install -r requirements.txt