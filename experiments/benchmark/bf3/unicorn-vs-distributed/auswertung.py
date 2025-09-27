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

throughputs = {"baseline": Datastore(), "distributed": Datastore()}

for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, newline='') as csvfile:
            #print(f"Processing file: {filename}")
            reader = csv.reader(csvfile, delimiter=';')
            db_type = "distributed" if "dma" in filename else "baseline"
            for row in reader:
                if row[Rows.PHASE.value] == "load" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value]:
                    throughputs[db_type].add_load_throughput(float(row[Rows.VALUE.value]))
                elif row[Rows.PHASE.value] == "run" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value] :
                    throughputs[db_type].add_throughput(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))

def create_plot():
    workloads = ["Load", "a", "b", "c", "d"]
    db_types = ["baseline", "distributed"]
    x = np.arange(len(workloads))
    width = 0.18

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, db_type in enumerate(db_types):
        means = []
        stds = []
        ds = throughputs[db_type]
        for w in workloads:
            if w == "Load":
                means.append(np.mean(ds.throughputs[0]) if ds.throughputs[0] else 0)
                stds.append(np.std(ds.throughputs[0]) if ds.throughputs[0] else 0)
            else:
                means.append(ds.get_mean(w))
                stds.append(ds.get_std(w))
        bar_tag = "Distributed Database" if db_type == "distributed" else "Baseline"
        bars = ax.bar(x + i * width, means, width, yerr=stds, label=f"Database: {bar_tag}")
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

    # Set x-ticks between the two bars for each workload
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(["Load Phase", "Workload A", "Workload B", "Workload C", "Workload D"])
    ax.set_ylabel('Throughput (ops/sec)')
    ax.set_title('Comparison of Baseline Fjall and the Distributed Database by Throughput')
    ax.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig('throughput_comparison-bl-distributed.png')  # Save the plot as a PNG file

create_plot()