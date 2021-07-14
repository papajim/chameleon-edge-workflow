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

CONDOR_INSTALL_DIR=/home/condor/htcondor
cat /home/condor/50-test-setup.conf >> $CONDOR_INSTALL_DIR/etc/condor_config
if [[ $TOKEN ]]; then
    mkdir $CONDOR_INSTALL_DIR/tokens.d
    echo "SEC_TOKEN_SYSTEM_DIRECTORY = $CONDOR_INSTALL_DIR/tokens.d" >> $CONDOR_INSTALL_DIR/etc/condor_config
    echo "$TOKEN" > $CONDOR_INSTALL_DIR/tokens.d/isi_token

    # token auth
    chmod 600 $CONDOR_INSTALL_DIR/tokens.d/isi_token
fi 

if [[ $CONDOR_HOST ]]; then
    echo "CONDOR_HOST = $CONDOR_HOST" >> $CONDOR_INSTALL_DIR/etc/condor_config
fi

source /home/condor/htcondor/condor.sh
cat /home/condor/htcondor/condor.sh >> ~/.bashrc

exec "$@"
