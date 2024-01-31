#!/bin/bash

# Usage:
# main.sh <process amount>

# find process amount
process_amount=2

if [ -n "$1" ]; then
    process_amount=$1
fi
echo ">>> Process amount $process_amount"

rm ./stethoscope.log

export PYTHONPATH=`pwd` && \
mpiexec -n $process_amount \
    python ./main.py \
        --configFile=./stethoscope_config_localtest.ini
