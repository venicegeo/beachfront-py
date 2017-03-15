# beachfront-py
# https://github.com/venicegeo/beachfront-py

# Copyright 2016, RadiantBlue Technologies, Inc.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

FROM debian:latest

RUN apt-get update; \
    apt-get install -y python-setuptools python-numpy python-dev libgdal-dev python-gdal swig git g++; \
    apt-get install -y libagg-dev libpotrace-dev; \
    easy_install pip; pip install wheel;

WORKDIR /work
COPY requirements.txt /work/requirements.txt
COPY requirements-dev.txt /work/requirements-dev.txt

RUN \
    pip install -r requirements.txt; \
    pip install -r requirements-dev.txt;
