#!/usr/bin/python3
import csv
import json
import os

workloads = ["a", "b", "c"]

fieldnames = ["service", "workload", "load/run", "metric", "measurement", "value"]
data = []

for s in ["baseline", "dma_copy", "baseline-rocks"]:
    if not os.path.exists(f"./{s}"):
        print(f"Directory {s} does not exist, skipping...")
        continue
    for workload in workloads:
        for op in ["load", "run"]:
            filename = f"./{s}/{op}_workload{workload}.json"
            if not os.path.exists(filename):
                print(f"File {filename} does not exist, skipping...")
                continue
            
            with open(filename, "r") as f:
                json_data = json.load(f)
                for entry in json_data:
                    current = [s, workload, op, entry["metric"], entry["measurement"], entry["value"]]
                    if entry["metric"] == "OVERALL" and "Throughput" in entry["measurement"]:
                        print(current)
                    data.append(current)



with open('experiment-results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(fieldnames)
    writer.writerows(data)