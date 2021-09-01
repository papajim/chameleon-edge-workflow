#!/usr/bin/env python3
import argparse
import os
import shutil
import sys

from pathlib import Path

import htcondor
import classad
from htcondor import dags

def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Create a fork join workflow")
    parser.add_argument(
                "num_levels",
                type=int,
                choices=range(1, 101),
                metavar="[1,100]",
                help="number of levels in the workflow"
            )

    parser.add_argument(
                "layer_width",
                type=int,
                choices=range(1,101),
                metavar="[1,100]",
                help="number of independent jobs per odd numbered layer"
            )

    parser.add_argument(
                "job_duration",
                type=int,
                choices=range(1, 301),
                metavar="[1,300]",
                help="duration in seconds that a job will sleep for in"
            )

    return parser.parse_args(args)

def build_dag(num_layers, layer_width, job_duration):
    dag = dags.DAG()

    sub = htcondor.Submit(
        executable="/bin/sleep",
        arguments=job_duration,
        **{"+mycustomattr": classad.quote("helloworld_$(num)")}
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
    return dag

if __name__=="__main__":
    args = parse_args()

    dag = build_dag(args.num_levels, args.layer_width)

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

