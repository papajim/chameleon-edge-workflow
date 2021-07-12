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

#export CONDOR_CONFIG=/home/condor/50-test-setup.conf
#/work/htcondor/release_dir/sbin/condor_store_cred -f \
#     /home/condor/htcondor/etc/pool_password -p kevinMalone

#cat /home/condor/50-test-setup.conf >> /home/condor/htcondor/etc/condor_config
CONDOR_INSTALL_DIR=/home/condor/htcondor
if [[ $TOKEN ]]; then
    mkdir $CONDOR_INSTALL_DIR/tokens.d
    echo "$TOKEN" > $CONDOR_INSTALL_DIR/tokens.d/isi_token

    # token auth
    chmod 600 $CONDOR_INSTALL_DIR/tokens.d/isi_token
fi 

source /home/condor/htcondor/condor.sh
cat /home/condor/htcondor/condor.sh >> ~/.bashrc

exec "$@"
