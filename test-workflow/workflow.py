#!/usr/bin/env python3
import logging
from pathlib import Path

from Pegasus.api import *

logging.basicConfig(level=logging.INFO)

CURRENT_DIR = Path(__file__).resolve().parent

props = Properties()
props["pegasus.mode"] = "development"
props.write()

rc = ReplicaCatalog()
rc.add_replica(site="local", lfn="input.txt", pfn=CURRENT_DIR / "input.txt")
rc.write()

tc = TransformationCatalog()
cat = Transformation(
            "cat.sh",
            site="local",
            pfn=CURRENT_DIR / "bin/cat.sh",
            is_stageable=True
        )

# override existing worker package so we can use the arm one
pegasus_worker = Transformation(
            "worker",
            namespace="pegasus",
            site="isi",
            pfn="https://download.pegasus.isi.edu/arm-worker-packages/pegasus-worker-5.0.1dev-aarch64_deb_10.tar.gz",
            is_stageable=True
        )

tc.add_transformations(cat, pegasus_worker)
tc.write()

wf = Workflow("test")
cat_job = Job(cat)\
            .add_inputs(File("input.txt"))\
            .add_outputs(File("output.txt"))\
            .add_condor_profile(requirements='Arch == "aarch64"')

wf.add_jobs(cat_job)

wf.plan(submit=True)
