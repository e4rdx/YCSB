# Thesis Fork of YCSB

## Setup
1. Install python3, java, and maven.
2. Run the experiment using one of the scripts with the required parameters. The available scripts are:
   - `experiment-baseline.sh`: Use this script to benchmark the baseline Fjall.
   - `experiment-rocks.sh`: This script benchmarks the RocksDB Baseline variant.
   - `run-experiment-dlsm.sh`: Use this script to benchmark the distributed Database variant.

## Processing Results
The results will be stored in the experiments directory. To generate a .csv file, use the process_results.py script. This script will create a CSV file from the JSON results.