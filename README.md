# Thesis Fork of YCSB

## Setup
1. Install python3, java, and maven. For creating plots, you will also need matplotlib and numpy.
2. Run the experiment using one of the scripts with the required parameters. The available scripts are:
   - `experiment-baseline.sh`: Use this script to benchmark the baseline Fjall.
   - `experiment-rocks.sh`: This script benchmarks the RocksDB Baseline variant.
   - `run-experiment-dlsm.sh`: Use this script to benchmark the distributed Database variant.

## Processing Results
The results will be stored in the experiments directory. To generate a .csv file, use the process_results.py script. This script will create a CSV file from the JSON results.

## Creating Plots
To create the plots, move the generated CSV file into one of the subdirectories of experiments/benchmark. Then rename the CSV file according to the naming scheme used in the scripts.
Finally, run the auswertung.py script. This will generate a PNG file with the plot.
In the benchmark directories, there are already some example CSV files so that you can directly run the auswertung.py script to see how it works.

## Flamegraphs
The flamegraphs can also be found in the experiments/benchmark/flamegraphs directory.