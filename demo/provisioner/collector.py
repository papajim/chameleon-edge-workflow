#!/usr/bin/env python3
import htcondor
import classad

col = htcondor.Collector()
slots = col.query(
            htcondor.AdTypes.Startd,
            projection=["Name", "Activity", "State", "Arch"]
        )


'''
condor has a "post dead" option where you can call a script
after the worker has been shutdown
'''
# num unclaimed and idle per architecture
result = {"X86_64": 0, "aarch64": 0}
for s in slots:
    arch = s["Arch"]
    state = s["State"]
    activity = s["Activity"]

    if state == "Unclaimed" and activity == "Idle":
        result[arch] += 1

print(result)


