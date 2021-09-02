#!/usr/bin/env python3
import os
import time
import sys
import shutil
import enum

from collections import namedtuple
from pathlib import Path
from typing import Dict

import htcondor
import classad

from htcondor import dags

class JobStatus(enum.Enum):
    UNEXPANDED = 0
    IDLE = 1
    RUNNING = 2
    REMOVED = 3
    COMPLETED = 4
    HELD = 5
    SUBMISSION_ERR = 6

class Arch(enum.Enum):
    X86_64 = "X86_64"
    ARM64 = "AARCH64"

def get_available_slots(col: htcondor.Collector) -> Dict:
    """
    A a dict of available slots per architecture in the format:

    {
        "X86_64": <int>,
        "AARCH64": <int>,
        "other": <int>,
        "unavailable": <int>
    }


    :param col: collector to query
    :type col: htcondor.Collector
    :return: dict of available/unavailable slots
    :rtype: Dict
    """

    result = {
        Arch.X86_64.value: 0,
        Arch.ARM64.value: 0,
        "other": 0,
        "unavailable": 0
    }

    num_total_available = 0
    
    slots = col.query(
        htcondor.AdTypes.Startd,
        projection=["Name", "Activity", "State", "Arch"]
    )

    for s in slots:
        arch = s["Arch"]
        state = s["State"]
        activity = s["Activity"]

        if state == "Unclaimed" and activity == "Idle":
            if arch in result:
                result[arch] += 1
            else:
                result["other"] += 1
            
            num_total_available += 1
        else:
            result["unavailable"] += 1
    
    return result

class Provisioner:
    QueueState = namedtuple("QueryState", ["idle", "running"])
    PoolState = namedtuple("PoolState", [Arch.X86_64.value, Arch.ARM64.value, "unavailable"])
    
    def __init__(condor_host: str, token_dir: str):
        self.condor_host = condor_host
        self.token_dir = token_dir
        
        self.docker = docker.from_env()
        self.collector = htcondor.Collector()
        self.schedd = self.collector.locate(htcondor.DaemonTypes.Schedd)

    def get_queue_state(self) -> Provisioner.QueueState:
        result = Provisioner.QueueState(idle=0, running=0)
        pass

    
    def get_pool_state(self) -> Provisioner.PoolState:
        """Get the count of available and unvailable slots per architecture.

        :raises RuntimeError: encountered unexpected arch
        :return: current state of the pool 
        :rtype: Provisioner.PoolState
        """
        result = PoolState(X86_64=0, ARM64=0, unavailable=0)
        
        slots = col.query(
            htcondor.AdTypes.Startd,
            projection=["Name", "Activity", "State", "Arch"]
        )

        for s in slots:
            arch = s["Arch"]
            state = s["State"]
            activity = s["Activity"]

            if state == "Unclaimed" and activity == "Idle":
                if arch == Arch.X86_64.value:
                    result.X86_64 += 1
                elif arch == Arch.ARM64.value:
                    result.ARM64 += 1
                else:
                    raise RuntimeError("did not expect arch: {}".format(arch))
            else:
                result.unavailable += 1
        
        return result

    def run(self):
        pass

    def print_state(self, slots: Dict[str, int], queue: htcondor.QueryIterator):
        pass

coll = htcondor.Collector()
schedd_ad = coll.locate(htcondor.DaemonTypes.Schedd)
print(schedd_ad)

schedd = htcondor.Schedd(schedd_ad)

for i in range(300):
    print("i={}".format(i))
    time.sleep(3)

    print("condor_q {}".format("*"*50))
    for job in schedd.xquery(projection=["ClusterId", "ProcId", "JobStatus", "mycustomattr"]):
        print(job["ClusterId"], job["ProcId"], job["JobStatus"], job.get("mycustomattr"))


'''
JobStatus in job ClassAds

0	Unexpanded	U
1	Idle	I
2	Running	R
3	Removed	X
4	Completed	C
5	Held	H
6	Submission_err	E

output:
# use mycustom attr to signify architecture type since we can't easly use requirements expr
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 2; ProcId = 1; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 2; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 3; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 4; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 5; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 6; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 7; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 8; ClusterId = 6 ]
[ ServerTime = 1629507402; mycustomattr = "helloworld"; JobStatus = 1; ProcId = 9; ClusterId = 6 ]
'''

'''
can config condor that if it is idle for x amount of minutes, it will shutdown 
'''

class Provisioner:
    def __init__(self):
        pass    
