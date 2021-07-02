FROM ryantanaka/saved-condor9.1

RUN apt update && apt install -y supervisor

# setup non root user to run condor daemons
RUN adduser --disabled-password --gecos "" condor

# install condor
RUN cd /work/htcondor/release_dir \
    && ./condor_configure \
        --install=/work/htcondor/release_dir \
        --install-dir=/usr \
        --type=execute \
        --owner=condor \
        --overwrite \
        --install

# use same configs as other nodes
COPY ./condor9-configs.tar.gz /etc/condor/
RUN cd /etc/condor && tar -xzvf condor9-configs.tar.gz
COPY ./50-test-setup.conf /etc/condor/config.d/50-test-setup.conf
RUN condor_store_cred -f /etc/condor/pool_password -p kevinMalone

# supervisor configs
COPY ./supervisord.conf /etc/supervisor/supervisord.conf
COPY ./condor-supervisor.conf /etc/supervisor/conf.d/condor-supervisor.conf

# setup entrypoint script
COPY ./entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod u+x /usr/bin/entrypoint.sh

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
CMD ["/usr/bin/supervisord"]
