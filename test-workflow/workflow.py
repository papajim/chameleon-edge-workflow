#!/usr/bin/env python3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

CURRENT_DIR = Path(__file__).resolve().parent

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
tc.add_transformations(cat)
tc.write()

wf = Workflow("test")
cat_job = Job(cat)\
            .add_inputs(File("input.txt"))\
            .add_outputs(File("output.txt"))\
            .add_env(PEGASUS_HOME="/home/condor/pegasus-5.1.0dev")\
            .add_condor_profile(requirements="Arch == aarch64")

wf.add_jobs(cat_job)

wf.plan(submit=True)
