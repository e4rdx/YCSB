#!/bin/bash

while getopts t:b:d:h: flag
do
    case "${flag}" in
        t) threads=${OPTARG};;
        b) baseline=${OPTARG};;
        d) dpu=${OPTARG};;
        h) echo "Usage: $0 [-t <threads=5>] -b <baseline> -d <dpu>"
           echo "-h Prints this help message and exits"
           echo "-t Number of threads to use for the experiment (default: 5)"
           echo "Example: $0 -b http://192.168.100.60:8080 -d http://192.168.100.62:8080"
           exit 0;;
    esac
done

if [ -z "$threads" ]; then
    threads=5
fi

if [ -z "$baseline" ]; then
    echo "Please provide the baseline api url using -b option"
    exit 1
fi
if [ -z "$dpu" ]; then
    echo "Please provide the DPU api url IP using -d option"
    exit 1
fi

echo "Using $threads threads for the experiment"

# Cleanup
rm -r experiments/baseline
rm -r experiments/dma_copy

echo "Please start the baseline experiment on the host using 'cargo run --release -- -c' and press Enter to continue..."
read -r

# check if ../experiments/baseline exists
if [ ! -d "experiments/baseline" ]; then
  echo "Creating directory experiments/baseline"
  mkdir -p experiments/baseline
fi

# loop over all workloads
for workload in a b c; do
    # Load data
    python3 bin/ycsb load thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${baseline}
    cp experiments/workload${workload}.json experiments/baseline/load_workload${workload}.json

    # Run experiment
    python3 bin/ycsb run thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${baseline}
    cp experiments/workload${workload}.json experiments/baseline/run_workload${workload}.json

    echo "Please reset the database and press Enter to continue..."
    read -r
done



echo "Now start dma copy on the host and the dpu"
echo "On the host, run: cargo run --release -- -c"
echo "On the DPU, run: cargo run --release -- --api-url=<http://host-ip:9090> -c"
echo "Then press Enter to continue..."
read -r

# check if ../experiments/dma_copy exists
if [ ! -d "experiments/dma_copy" ]; then
  echo "Creating directory experiments/dma_copy"
  mkdir -p experiments/dma_copy
fi

for workload in a b c; do
    # Load data
    python3 bin/ycsb load thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${dpu}
    cp experiments/workload${workload}.json experiments/dma_copy/load_workload${workload}.json

    # Run experiment
    python3 bin/ycsb run thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${dpu}
    cp experiments/workload${workload}.json experiments/dma_copy/run_workload${workload}.json

    echo "Please reset the database and press Enter to continue..."
    read -r
done