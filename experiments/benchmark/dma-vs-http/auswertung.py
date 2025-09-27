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

throughputs = {"dma": Datastore(), "network-sync": Datastore()}

for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, newline='') as csvfile:
            #print(f"Processing file: {filename}")
            reader = csv.reader(csvfile, delimiter=';')
            db_type = "network-sync" if "network-sync" in filename else "dma"
            for row in reader:
                if row[Rows.PHASE.value] == "load" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value]:
                    throughputs[db_type].add_load_throughput(float(row[Rows.VALUE.value]))
                elif row[Rows.PHASE.value] == "run" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value] :
                    throughputs[db_type].add_throughput(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))

def create_plot():
    db_types = ["dma", "network-sync"]
    x = np.arange(len(db_types))
    width = 0.5  # Make bars closer together

    fig, ax = plt.subplots(figsize=(6, 5))

    means = [np.mean(throughputs[db].throughputs[0]) if throughputs[db].throughputs[0] else 0 for db in db_types]
    stds = [np.std(throughputs[db].throughputs[0]) if throughputs[db].throughputs[0] else 0 for db in db_types]

    bar_tags = ["DMA", "HTTP-Requests"]
    colors = ['#1f77b4', '#ff7f0e']  # Different colors for bars

    bars = ax.bar(x, means, width, yerr=stds, label=bar_tags, color=colors, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(bar_tags)
    ax.set_ylabel('Load Throughput (ops/sec)')
    ax.set_title('Load Throughput Comparison')
    ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7, zorder=0)
    ax.legend()

    plt.tight_layout()
    #plt.show()
    plt.savefig('dma-vs-http.png')

create_plot()