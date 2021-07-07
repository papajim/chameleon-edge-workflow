FROM htcondor/execute:9.1-el7

# configuration for test pool
RUN echo -e '#--     Authentication settings\n\
SEC_PASSWORD_FILE = /etc/condor/pool_password\n\
SEC_DEFAULT_AUTHENTICATION = REQUIRED\n\
SEC_DEFAULT_AUTHENTICATION_METHODS = FS,PASSWORD\n\
SEC_READ_AUTHENTICATION = OPTIONAL\n\
SEC_CLIENT_AUTHENTICATION = OPTIONAL\n\
SEC_ENABLE_MATCH_PASSWORD_AUTHENTICATION = TRUE\n\
DENY_WRITE = anonymous@*\n\
DENY_ADMINISTRATOR = anonymous@*\n\
DENY_DAEMON = anonymous@*\n\
DENY_NEGOTIATOR = anonymous@*\n\
DENY_CLIENT = anonymous@*\n\
\n\
#-- With strong security, do not use IP based controls\n\
HOSTALLOW_WRITE = *\n\
ALLOW_NEGOTIATOR = *\n\
# dynamic slots\n\
SLOT_TYPE_1 = cpus=100%,disk=100%,swap=100%\n\
SLOT_TYPE_1_PARTITIONABLE = TRUE\n\
NUM_SLOTS = 1\n\
NUM_SLOTS_TYPE_1 = 1\n'\
> /etc/condor/config.d/50-test-setup.conf

RUN condor_store_cred -f /etc/condor/pool_password -p kevinMalone

