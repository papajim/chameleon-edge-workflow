#!/usr/bin/env python3
import os
import time
import sys
import shutil

from pathlib import Path

import htcondor
import classad

from htcondor import dags

coll = htcondor.Collector()
schedd_ad = coll.locate(htcondor.DaemonTypes.Schedd)
print(schedd_ad)

schedd = htcondor.Schedd(schedd_ad)

for i in range(300):
    print("i={}".format(i))
    time.sleep(3)

    print("condor_q {}".format("*"*50))
    for job in schedd.xquery(projection=["ClusterId", "ProcId", "JobStatus", "mycustomattr"]):
        print(repr(job))


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


