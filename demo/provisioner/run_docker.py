#!/usr/bin/env python3
import signal
import time

import docker

client = docker.from_env()
containers = list()
for i in range(1):
    c = client.containers.run(
            image="ryantanaka/condor9-x86_64-isi-demo-worker",
            volumes=["/local-scratch/tanaka/condorexec/secrets:/root/secrets:ro"],
            environment={"CONDOR_HOST":"workflow.isi.edu",},
            remove=True,
            name="worker-{i}".format(i=i),
            detach=True
        )

    print("created {}".format(c))
    containers.append(c)

time.sleep(120)

for c in containers:
    print("killing {}".format(c))
    print(c.kill(signal=signal.SIGINT))

