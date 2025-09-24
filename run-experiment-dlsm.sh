#!/bin/bash

while getopts t:d:h: flag
do
    case "${flag}" in
        t) threads=${OPTARG};;
        d) dpu=${OPTARG};;
        h) echo "Usage: $0 [-t <threads=5>] -b <baseline> -d <dpu>"
           echo "-h Prints this help message and exits"
           echo "-t Number of threads to use for the experiment (default: 5)"
           echo "Example: $0 -d http://192.168.100.62:8080"
           exit 0;;
    esac
done

if [ -z "$threads" ]; then
    threads=50
fi

if [ -z "$dpu" ]; then
    echo "Please provide the DPU api url IP using -d option"
    exit 1
fi

echo "Using $threads threads for the experiment"

# Cleanup
echo "Cleaning up previous experiment results..."
read -p "Press Enter to continue or Ctrl+C to abort..."
rm -r experiments/baseline
rm -r experiments/baseline-rocks
rm -r experiments/dma_copy

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

for workload in a b c d; do
    # Only load data if workload is not 'd'
    if [ "$workload" != "d" ]; then
        python3 bin/ycsb load thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${dpu}
        cp experiments/workload${workload}.json experiments/dma_copy/load_workload${workload}.json
    fi

    # Run experiment
    python3 bin/ycsb run thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${dpu} -p thesis.get=http
    cp experiments/workload${workload}.json experiments/dma_copy/run_workload${workload}.json

    #curl -X POST http://192.168.100.203:8080/api/info

    # Only ask for reset after 'a' and 'b'
    if [ "$workload" = "a" ] || [ "$workload" = "b" ]; then
        echo "Please reset the database and press Enter to continue..."
        read -r
    fi
done