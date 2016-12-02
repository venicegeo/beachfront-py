FROM debian:jessie

WORKDIR /work
COPY requirements.txt /work/requirements.txt
COPY requirements-dev.txt /work/requirements-dev.txt

RUN apt-get update; \
    apt-get install -y python-pip python-numpy python-dev libgdal-dev python-gdal swig git; \
    apt-get install -y libagg-dev libpotrace-dev;

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
