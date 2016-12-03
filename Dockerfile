# beachfront-py
# https://github.com/venicegeo/beachfront-py

# Copyright 2016, RadiantBlue Technologies, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
