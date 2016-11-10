#!/bin/bash

yum install -y epel-release
yum -y update

yum install -y python-pip numpy python-devel gdal-devel gdal-python swig git wget gcc-c++
pip install wheel

# potrace
yum install -y agg-devel potrace-devel

# install app
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install .

# run tests
nosetests test -v -s
