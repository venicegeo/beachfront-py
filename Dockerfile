FROM ubuntu:14.04

WORKDIR /work
COPY requirements.txt /work/requirements.txt
COPY requirements-dev.txt /work/requirements-dev.txt

RUN apt-get update; \
    apt-get install -y python-pip libagg-dev libpotrace-dev python-numpy python-dev libgdal-dev gdal-bin swig git python-gdal libfreetype6-dev; \
    pip install cython;
    #pip install numpy;

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
