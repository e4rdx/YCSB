#!/bin/bash

THREADS=5

# Cleanup
rm -rf experiments/baseline
rm -rf experiments/dma_copy

echo "Please start the baseline experiment on the server and press Enter to continue..."
read -r

# check if ../experiments/baseline exists
if [ ! -d "experiments/baseline" ]; then
  echo "Creating directory experiments/baseline"
  mkdir -p experiments/baseline
fi

# loop over all workloads
for workload in a b; do
    # Load data
    python3 bin/ycsb load thesis -threads $THREADS -P workloads/thesis_workload${workload} -p thesis.ip=http://192.168.100.60:8080
    cp experiments/workload${workload}.json experiments/baseline/load_workload${workload}.json

    # Run experiment
    python3 bin/ycsb run thesis -threads $THREADS -P workloads/thesis_workload${workload} -p thesis.ip=http://192.168.100.60:8080
    cp experiments/workload${workload}.json experiments/baseline/run_workload${workload}.json

    echo "Please reset the database and press Enter to continue..."
    read -r
done



echo "Now start dma copy on the server and press Enter to continue..."
read -r

# check if ../experiments/dma_copy exists
if [ ! -d "experiments/dma_copy" ]; then
  echo "Creating directory experiments/dma_copy"
  mkdir -p experiments/dma_copy
fi

for workload in a b; do
    # Load data
    python3 bin/ycsb load thesis -threads $THREADS -P workloads/thesis_workload${workload} -p thesis.ip=http://192.168.100.203:8080
    cp experiments/workload${workload}.json experiments/dma_copy/load_workload${workload}.json

    # Run experiment
    python3 bin/ycsb run thesis -threads $THREADS -P workloads/thesis_workload${workload} -p thesis.ip=http://192.168.100.203:8080
    cp experiments/workload${workload}.json experiments/dma_copy/run_workload${workload}.json

    echo "Please reset the database and press Enter to continue..."
    read -r
done