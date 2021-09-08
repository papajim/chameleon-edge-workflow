FROM htcondor/execute:el7

# add custom attribute
RUN printf "DEMO_NODE = true\nSTARTD_ATTRS = \$(STARTD_ATTRS) DEMO_NODE" \
    > /root/config/custom.conf
