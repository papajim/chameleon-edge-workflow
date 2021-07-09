#!/bin/bash

# Builds three condor8 arm64 docker images, one for the following roles:
# central manager, submit, and execute. The configuration used for each
# role is located in ./configuration

set -e

for conf in ./configuration/*.conf;
do
    # create conf file to be passed into docker image
    cat $conf > ./50-test-setup.conf
    filename=$(basename -- $conf)
    image_name="ryantanaka/condor8-arm64-${filename%.*}"

    # build image for arm64
    echo "building: $image_name using configuration: $conf"
    docker buildx  build --platform linux/arm64 -t $image_name --progress=plain --push . 
done;

# cleanup
echo "removing ./50-test-setup.conf"
rm ./50-test-setup.conf

