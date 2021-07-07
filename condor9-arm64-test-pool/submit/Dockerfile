FROM ryantanaka/saved-condor9.1

RUN apt update && apt install -y supervisor

# setup non root users to run condor daemons and submit jobs
RUN adduser --disabled-password --gecos "" condor
RUN adduser --disabled-password --gecos "" submituser 

# add sample job to run
COPY ./test-job /home/submituser/test-job
RUN chown -R submituser /home/submituser/test-job

# use same configs as other nodes
RUN mkdir -p /home/condor
COPY ./50-test-setup.conf /home/condor/

# supervisor configs
COPY ./supervisord.conf /etc/supervisor/supervisord.conf
COPY ./condor-supervisor.conf /etc/supervisor/conf.d/condor-supervisor.conf

COPY ./entrypoint.sh /home/condor/entrypoint.sh
RUN chmod u+x /home/condor/entrypoint.sh

EXPOSE 9618

ENTRYPOINT ["/home/condor/entrypoint.sh"]
CMD ["/usr/bin/supervisord"]
