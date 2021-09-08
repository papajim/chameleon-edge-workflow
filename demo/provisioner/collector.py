#!/usr/bin/env python3
import time
import os
import htcondor
import classad

col = htcondor.Collector()
while True:
    slots = col.query(
                htcondor.AdTypes.Startd,
                projection=["Name", "Activity", "State", "Arch"]
            )

    # num unclaimed and idle per architecture
    result = {"X86_64": 0, "aarch64": 0}
    num_total_available = 0
    for s in slots:
        arch = s["Arch"]
        state = s["State"]
        activity = s["Activity"]

        if state == "Unclaimed" and activity == "Idle":
            result[arch] += 1
            num_total_available += 1

    for arch, count in result.items():
        print("{0:>15}: {1} {2}".format(arch, "{} ".format(chr(9605))*count, count))

    print("{0:>15}: {1} {2}".format(
                    "Unavailable", 
                    "{} ".format(chr(9605)) * (len(slots) - num_total_available), 
                    len(slots) - num_total_available
                )
            )

    time.sleep(1)
    os.system("clear")


