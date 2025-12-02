# use an official python runtime as a parent image
FROM python:3.10-slim-bookworm

# fix python printing
ENV PYTHONUNBUFFERED 1

# installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/production.txt

# copy project to docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/
