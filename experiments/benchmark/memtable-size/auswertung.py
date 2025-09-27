import matplotlib.pyplot as plt
import numpy as np
import csv
import os
from enum import Enum

class Rows(Enum):
    SERVICE = 0
    WORKLOAD = 1
    PHASE = 2
    METRIC = 3
    MEASUREMENT = 4
    VALUE = 5

class Datastore:
    def __init__(self):
        self.throughputs = [[] for _ in range(5)]
        self.workloads = {"a": 1, "b": 2, "c": 3, "d": 4}
    
    def add_load_throughput(self, value):
        self.throughputs[0].append(value)
    
    def resolve_workload(self, workload):
        return self.workloads[workload]
    
    def add_throughput(self, workload, value):
        self.throughputs[self.resolve_workload(workload)].append(value)

    def get_mean(self, workload):
        idx = self.resolve_workload(workload)
        return np.mean(self.throughputs[idx]) if self.throughputs[idx] else 0

    def get_std(self, workload):
        idx = self.resolve_workload(workload)
        return np.std(self.throughputs[idx]) if self.throughputs[idx] else 0

throughputs = {"4": Datastore(), "8": Datastore(), "16": Datastore(), "24": Datastore(), "32": Datastore()}

for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, newline='') as csvfile:
            #print(f"Processing file: {filename}")
            reader = csv.reader(csvfile, delimiter=';')
            memtable_size = filename.split('-')[0]
            for row in reader:
                if row[Rows.PHASE.value] == "load" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value]:
                    throughputs[memtable_size].add_load_throughput(float(row[Rows.VALUE.value]))
                elif row[Rows.PHASE.value] == "run" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value] :
                    throughputs[memtable_size].add_throughput(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))

def create_plot():
    workloads = ["Load", "a", "b", "c", "d"]
    memtable_sizes = ["4", "8", "16", "24", "32"]
    x = np.arange(len(workloads))
    width = 0.18

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, mem_size in enumerate(memtable_sizes):
        means = []
        stds = []
        ds = throughputs[mem_size]
        for w in workloads:
            if w == "Load":
                means.append(np.mean(ds.throughputs[0]) if ds.throughputs[0] else 0)
                stds.append(np.std(ds.throughputs[0]) if ds.throughputs[0] else 0)
            else:
                means.append(ds.get_mean(w))
                stds.append(ds.get_std(w))
        bars = ax.bar(x + i * width, means, width, yerr=stds, label=f"Memtable size {mem_size}MB")
        # Add grid lines behind bars
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

    ax.set_ylabel('Throughput (ops/sec)')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(["Load Phase", "Workload A", "Workload B", "Workload C", "Workload D"])
    ax.set_title('Throughput by Workload and Memtable Size')
    ax.legend()
    plt.tight_layout()
    plt.savefig('comparison_memtable_size.png')
    plt.show()

create_plot()