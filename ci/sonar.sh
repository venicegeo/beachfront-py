#!/bin/bash -ex

#pushd `dirname $0`/.. > /dev/null
#root=$(pwd -P)
#popd > /dev/null

#source $root/ci/vars.sh

## docker

docker info
pip install docker-compose==1.8.0

## build docker image

docker-compose build

## Install Dependencies ########################################################

#pip install -r requirements.txt

## Run Tests ###################################################################

#coverage run --source=beachfront -m unittest discover
#coverage xml -o report/coverage/coverage.xml
#coverage html -d report/coverage/html
#coverage report
