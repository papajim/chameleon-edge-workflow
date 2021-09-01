#!/bin/bash

docker run \
    -v ~/condorexec/secrets:/root/secrets:ro \
    --name=htcondor-execute \
    --cpus=1 \
    -e CONDOR_HOST=workflow.isi.edu \
    -e NUM_CPUS=2 \
    -e MEMORY=1024 \
    --rm \
    htcondor/execute:el7
