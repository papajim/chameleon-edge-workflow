#!/bin/sh
CONDOR_CONFIG="//etc/condor_config"
export CONDOR_CONFIG
PATH="//bin://sbin:$PATH"
export PATH
if [ "X" != "X${PYTHONPATH-}" ]; then
  PYTHONPATH="//lib/python:$PYTHONPATH"
else
  PYTHONPATH="//lib/python"
fi
export PYTHONPATH

exec "$@"
