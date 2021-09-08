#!/usr/bin/env python3
import os
import time
import sys
import shutil
import enum
import signal
import argparse

from collections import namedtuple
from pathlib import Path
from typing import Dict

import docker

import htcondor
import classad

from htcondor import dags

# custom attribute we will use to specify arch 
ARCH_CUSTOM_ATTRIBUTE = "REQUIRED_ARCH"

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
    AARCH64 = "AARCH64"

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
        Arch.AARCH64.value: 0,
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

    class QueueState:
        class Count:
            def __init__(self):
                self.idle = 0
                self.running = 0

            def __repr__(self):
                return "Count(idle={}, running={})".format(self.idle, self.running)

        def __init__(self):
            self.X86_64 = self.Count()
            self.AARCH64 = self.Count()

        def __str__(self):
            return "QueueState: X86_64={}, AARCH64={}".format(self.X86_64, self.AARCH64)

    class PoolState:
        def __init__(self):
            self.X86_64 = 0
            self.AARCH64 = 0
            self.unavailable = 0

        def __str__(self):
            return "PoolState: X86_64={}, AARCH64={}, unavailable={}".format(
                    self.X86_64,
                    self.AARCH64,
                    self.unavailable
                )

    
    def __init__(self, condor_host: str = None, token_dir: str = None):
        self.condor_host = condor_host
        self.token_dir = token_dir
        
        self.docker = docker.from_env()

        self.collector = htcondor.Collector()
        self.schedd_ad = self.collector.locate(htcondor.DaemonTypes.Schedd)
        self.schedd = htcondor.Schedd(self.schedd_ad)

    def get_queue_state(self):
        """
        Current state of the queue. Returns number of idle and running jobs for
        x86_64 and ARM

        :return: number of idle and running jobs 
        :rtype: Provisioner.QueueState
        """

        # this doesn't account for for all jobs, only the ones for which we have
        # set the custom attribute: REQUIRED_ARCH
        result = self.QueueState()

        for job in self.schedd.xquery(projection=["ClusterId", "ProcId", "JobStatus", ARCH_CUSTOM_ATTRIBUTE]):
            required_arch = str(job.get(ARCH_CUSTOM_ATTRIBUTE))
            job_status = job["JobStatus"]

            if required_arch == Arch.X86_64.value:
                if job_status == JobStatus.IDLE.value: 
                    result.X86_64.idle += 1
                elif job_status == JobStatus.RUNNING.value:
                    result.X86_64.running += 1

            elif required_arch == Arch.AARCH64.value:
                if job_status == JobStatus.IDLE.value:
                    result.AARCH64.idle += 1
                elif job_status == JobStatus.RUNNING.value:
                    result.AARCH64.running += 1

        return result

    
    def get_pool_state(self):
        """
        Get the count of available and unvailable slots per architecture.

        :raises RuntimeError: encountered unexpected arch
        :return: current state of the pool 
        :rtype: Provisioner.PoolState
        """

        # THIS DOESN"T ACCOUNT FOR DYNAMIC SLOTS>........
        result = self.PoolState()
        
        slots = self.collector.query(
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
                elif arch == Arch.AARCH64.value:
                    result.AARCH64 += 1
                else:
                    raise RuntimeError("did not expect arch: {}".format(arch))
            else:
                result.unavailable += 1
        
        return result

    def provision(self, rate: int, ):
        '''
        {
            "hostname": {
                "state": <state>,
                "idle_duration": <duration>
            },
            ...
        }
        '''
        pass

    def monitor(self, rate: int):
        slots_str = "{0:>20} {1} {2}"
        bar = "{} ".format(chr(9605))
        while True:
            pool = self.get_pool_state()
            queue = self.get_queue_state()
            
            # print pool status information
            print("**** POOL *****************************")
            print(slots_str.format(Arch.X86_64.value, bar*pool.X86_64, pool.X86_64))
            print(slots_str.format(Arch.AARCH64.value, bar*pool.AARCH64, pool.AARCH64))
            print(slots_str.format("Unavailable", bar*pool.unavailable , pool.unavailable))

            # print queue status information
            print("**** JOBS *****************************")
            print(Arch.X86_64.value)
            print(slots_str.format("running", bar*queue.X86_64.running, queue.X86_64.running))
            print(slots_str.format("idle", bar*queue.X86_64.idle, queue.X86_64.idle))
            print(Arch.AARCH64.value)
            print(slots_str.format("running", bar*queue.AARCH64.running, queue.AARCH64.running))
            print(slots_str.format("idle", bar*queue.AARCH64.idle, queue.AARCH64.idle))

            time.sleep(rate)
            os.system("clear")

def build_and_submit_dag(num_layers, layer_width, job_duration):
    # TODO: support multiple different architectures (right now we just set
    # to x86_64
    dag = dags.DAG()

    sub = htcondor.Submit(
        executable="/bin/sleep",
        arguments=job_duration,
        **{"+{}".format(ARCH_CUSTOM_ATTRIBUTE): Arch.X86_64.value}
    )

    prev_layer = dag.layer(
                name="top",
                submit_description=sub
            )
    for i in range(1, num_layers):
        # odd layer is of width layer_width
        if i % 2 != 0:
            l = prev_layer.child_layer(
                        name="layer_{}".format(i),
                        submit_description=sub,
                        vars=[{"num":"{}_{}".format(i,x)} for x in range(layer_width)]
                    )
            prev_layer = l

        # even layer is of width 1
        else:
            l = prev_layer.child_layer(
                        name="layer_{}".format(i),
                        submit_description=sub,
                        vars=[{"num":"{}_{}".format(i,x)} for x in range(1)]
                    )
            prev_layer = l

    print(dag.describe())

    dag_path = Path.home() / "htcondor_dag"

    # blow away old files
    shutil.rmtree(dag_path, ignore_errors=True)

    dag_file = dags.write_dag(dag, dag_path)

    dag_submit = htcondor.Submit.from_dag(str(dag_file), {"force":True})
    print(dag_submit)

    coll = htcondor.Collector()
    schedd_ad = coll.locate(htcondor.DaemonTypes.Schedd)
    print(schedd_ad)

    schedd = htcondor.Schedd(schedd_ad)

    os.chdir(dag_path)
    with schedd.transaction() as txn:
        cluster_id = dag_submit.queue(txn)
    print("DAGMan job cluster is {}".format(cluster_id))
    os.chdir("..")

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="demo tools")

    subparsers = parser.add_subparsers(help="demo command to run")

    ### Monitor ##############################################################
    parser_monitor = subparsers.add_parser("monitor", help="monitor pool and queue")
    parser_monitor.set_defaults(cmd="monitor")
    parser_monitor.add_argument(
        "monitor_rate",
        type=int,
        default=None,
        choices=range(1, 300),
        metavar="[1,300]",
        help="rate, in seconds, at which to monitor condor_collector and schedd"
    )

    ### Provision ############################################################
    parser_provision = subparsers.add_parser("provision", help="start provisioner")
    parser_provision.set_defaults(cmd="provision")
    parser_provision.add_argument(
        "provision_rate",
        type=int,
        default=10,
        choices=range(1, 600),
        metavar="[1,600]",
        help="""rate, in seconds, at which to poll condor_collector and schedd 
        to decide if worker must be provisioned"""
    )

    parser_provision.add_argument(
        "condor_host",
        type=str,
        help="set CONDOR_HOST for worker containers that are started"
    )

    parser_provision.add_argument(
        "token_dir",
        type=str,
        help="""directory where condor token file exists, will be used to connect
        to condor host"""
    )

    ### Submit ###############################################################
    parser_submit = subparsers.add_parser("submit", help="submit forkjoin dag")
    parser_submit.set_defaults(cmd="submit")
    parser_submit.add_argument(
                "num_layers",
                type=int,
                choices=range(1, 101),
                metavar="[1,100]",
                help="number of levels in the workflow"
            )

    parser_submit.add_argument(
                "layer_width",
                type=int,
                choices=range(1,101),
                metavar="[1,100]",
                help="number of independent jobs per odd numbered layer"
            )

    parser_submit.add_argument(
                "job_duration",
                type=int,
                choices=range(1, 301),
                metavar="[1,300]",
                help="duration in seconds that a job will sleep for in"
            )

    return parser.parse_args(args)

if __name__=="__main__":
    # setup SIGINT handler
    def sigint_handler(signum, frame):
        print("got interrupt, exiting")
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)

    args = parse_args()

    if args.cmd == "monitor":
        Provisioner().monitor(args.monitor_rate)

    elif args.cmd == "provision":
        pass
    elif args.cmd == "submit":
        build_and_submit_dag(
                num_layers=args.num_layers, 
                layer_width=args.layer_width, 
                job_duration=args.job_duration
            )
    else:
        raise RuntimeError("unexpected cmd: {}".format(args.cmd))
