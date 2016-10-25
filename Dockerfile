FROM ubuntu:14.04

WORKDIR /work
COPY ./ /work

RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y python-pip python-dev libgdal-dev gdal-bin swig git
RUN pip install numpy
RUN pip install -r requirements.txt

RUN pip install .
