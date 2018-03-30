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

FROM developmentseed/geolambda:cloud

RUN \
    yum makecache fast; \
    yum install -y agg-devel;

#RUN apt-get update; \
#    apt-get install -y python-setuptools python-numpy python-dev libgdal-dev python-gdal swig git g++; \
#    apt-get install -y libagg-dev libpotrace-dev; \
#    easy_install pip; pip install wheel;

ENV \
    POTRACE_VERSION=1.14

# install potrace
RUN \
    wget http://potrace.sourceforge.net/download/$POTRACE_VERSION/potrace-$POTRACE_VERSION.tar.gz; \
    tar -xzvf potrace-$POTRACE_VERSION.tar.gz; \
    cd potrace-$POTRACE_VERSION; \
    ./configure --with-libpotrace; \
    make && make install && cd .. && \
    rm -rf potrace-$POTRACE_VERSION*

COPY requirements*txt $BUILD/

RUN \
    pip install -r requirements.txt; \
    pip install -r requirements-dev.txt
