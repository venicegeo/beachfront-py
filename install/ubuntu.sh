#!/bin/bash

apt-get update
apt-get install -y python-pip python-numpy python-dev libgdal-dev swig git python-gdal

# for potrace
apt-get install -y libagg-dev libpotrace-dev

# install app
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install .

# run tests
nosetest test -v -s
