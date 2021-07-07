#!/bin/bash
set -e
set -x

cd /work/htcondor/release_dir

./condor_configure \
    --type=execute \
    --owner=condor \
    --install=. \
    --install-dir=/home/condor/htcondor \
    --force \
    --verbose

export CONDOR_CONFIG=/home/condor/50-test-setup.conf
/work/htcondor/release_dir/sbin/condor_store_cred -f \
     /home/condor/htcondor/etc/pool_password -p kevinMalone

cat /home/condor/50-test-setup.conf >> /home/condor/htcondor/etc/condor_config

source /home/condor/htcondor/condor.sh
cat /home/condor/htcondor/condor.sh >> ~/.bashrc

exec "$@"
