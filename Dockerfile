FROM debian:latest

WORKDIR /work
COPY requirements.txt /work/requirements.txt
COPY requirements-dev.txt /work/requirements-dev.txt

RUN apt-get update; \
    apt-get install -y python-setuptools python-numpy python-dev libgdal-dev python-gdal swig git g++; \
    apt-get install -y libagg-dev libpotrace-dev; \
    easy_install pip; pip install wheel;

RUN \
    pip install cython; \
    pip install -r requirements.txt; \
    pip install -r requirements-dev.txt;
