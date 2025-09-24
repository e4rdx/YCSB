#!/bin/bash

while getopts t:b:h: flag
do
    case "${flag}" in
        t) threads=${OPTARG};;
        b) baseline=${OPTARG};;
        h) echo "Usage: $0 [-t <threads=5>] -b <baseline>"
           echo "-h Prints this help message and exits"
           echo "-t Number of threads to use for the experiment (default: 5)"
           echo "Example: $0 -b http://192.168.100.60:8080"
           exit 0;;
    esac
done

if [ -z "$threads" ]; then
    threads=50
fi

if [ -z "$baseline" ]; then
    echo "Please provide the baseline api url using -b option"
    exit 1
fi

echo "Using $threads threads for the experiment"

# Cleanup
echo "Cleaning up previous experiment results..."
read -p "Press Enter to continue or Ctrl+C to abort..."
rm -r experiments/baseline
rm -r experiments/baseline-rocks
rm -r experiments/dma_copy

echo "Please start the baseline experiment on the host using 'cargo run --release -- -c' and press Enter to continue..."
read -r

# check if ../experiments/baseline exists
if [ ! -d "experiments/baseline" ]; then
  echo "Creating directory experiments/baseline"
  mkdir -p experiments/baseline
fi

echo "Please start the baseline-rocks experiment on the host using 'cargo run --release -- -c' and press Enter to continue..."
read -r

# check if ../experiments/baseline-rocks exists
if [ ! -d "experiments/baseline-rocks" ]; then
  echo "Creating directory experiments/baseline-rocks"
  mkdir -p experiments/baseline-rocks
fi

for workload in a b c d; do
    # Load data
    if [ "$workload" != "d" ]; then
        python3 bin/ycsb load thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${baseline}
        cp experiments/workload${workload}.json experiments/baseline-rocks/load_workload${workload}.json
    fi

    # Run experiment
    python3 bin/ycsb run thesis -threads $threads -P workloads/thesis_workload${workload} -p thesis.ip=${baseline} -p thesis.get=http
    cp experiments/workload${workload}.json experiments/baseline-rocks/run_workload${workload}.json

    # Wait for reset after a and b only
    if [ "$workload" = "a" ] || [ "$workload" = "b" ]; then
        echo "Please reset the database and press Enter to continue..."
        read -r
    fi
done