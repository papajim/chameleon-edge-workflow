FROM ryantanaka/saved-condor9.1

RUN apt update && apt install -y supervisor

# setup non root user to run condor daemons
RUN adduser --disabled-password --gecos "" condor

# use same configs as other nodes
RUN mkdir -p /home/condor
COPY ./50-test-setup.conf /home/condor/

# supervisor configs
COPY ./supervisord.conf /etc/supervisor/supervisord.conf
COPY ./condor-supervisor.conf /etc/supervisor/conf.d/condor-supervisor.conf

COPY ./entrypoint.sh /home/condor/entrypoint.sh
RUN chmod u+x /home/condor/entrypoint.sh

# install pegasus worker package
COPY ./pegasus-worker-5.1.0dev-aarch64_deb_10.tar.gz /home/condor
RUN cd /home/condor \
    && tar -xzvf ./pegasus-worker-5.1.0dev-aarch64_deb_10.tar.gz

EXPOSE 9618

ENTRYPOINT ["/home/condor/entrypoint.sh"]
CMD ["/usr/bin/supervisord"]
