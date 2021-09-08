#!/bin/bash
set -e
set -x

# submit dag
python3 provisioner.py submit 5 5 30

# start montioring
python3 provisioner.py monitor 2

