FROM ubuntu:14.04

WORKDIR /work
COPY ./ /work

RUN apt-get update; \
    apt-get install -y python-pip python-dev libgdal-dev gdal-bin swig git; \
    pip install numpy;

RUN pip install -r requirements.txt

RUN pip install .
