FROM htcondor/execute:el7

# add custom attribute
RUN printf "DEMO_NODE = true\nSTARTD_ATTRS = \$(STARTD_ATTRS) DEMO_NODE\n" \
    > /root/config/custom.conf

RUN printf "NUM_SLOTS = 1\nNUM_SLOTS_TYPE_1 = 1\nSLOT_TYPE_1 = 100%%\nSLOT_TYPE_1_PARTITIONABLE = false" \
    >> /root/config/custom.conf

RUN rm /etc/condor/config.d/01-pslots.conf