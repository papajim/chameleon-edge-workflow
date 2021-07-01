FROM debian:buster

RUN apt-get update \
        && apt-get install -y \
        curl \
        wget \
        vim \
        supervisor

# install condor
ENV LIBCLASSAD14=/tmp/libclassad14-dev.deb
COPY ./condor-packages/libclassad14_8.8.13-1+deb10u0_arm64.deb $LIBCLASSAD14
RUN apt install -y $LIBCLASSAD14 \
    && rm $LIBCLASSAD14

ENV LIBCLASSAD_DEV=/tmp/libclassad-dev.deb
COPY ./condor-packages/libclassad-dev_8.8.13-1+deb10u0_arm64.deb $LIBCLASSAD_DEV
RUN apt install -y $LIBCLASSAD_DEV \
    && rm $LIBCLASSAD_DEV

ENV HTCONDOR=/tmp/htcondor.deb
COPY ./condor-packages/htcondor_8.8.13-1+deb10u0_arm64.deb $HTCONDOR
RUN apt install -y $HTCONDOR

# configuration for test pool
COPY ./50-test-setup.conf /etc/condor/config.d/50-test-setup.conf
RUN condor_store_cred -f /etc/condor/pool_password -p kevinMalone

# config to start up condor_master
COPY ./supervisord.conf /etc/supervisor/supervisord.conf
COPY ./10-htcondor.conf /etc/supervisor/conf.d/10-htcondor.conf

CMD ["/usr/bin/supervisord"] 


