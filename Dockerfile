# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ADD ./app /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
        gettext \
        xfonts-thai \
        gdal-bin libgdal-dev python3-gdal binutils libproj-dev \
        stunnel
RUN pip install -r requirements.txt
