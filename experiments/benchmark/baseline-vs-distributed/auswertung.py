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
        self.read_latencies = [[] for _ in range(5)]
        self.write_latencies = [[] for _ in range(5)]
    
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
    
    def add_read_latency(self, workload, value):
        self.read_latencies[self.resolve_workload(workload)].append(value)
    
    def get_read_mean(self, workload):
        idx = self.resolve_workload(workload)
        return np.mean(self.read_latencies[idx]) if self.read_latencies[idx] else 0
    
    def get_read_std(self, workload):
        idx = self.resolve_workload(workload)
        return np.std(self.read_latencies[idx]) if self.read_latencies[idx] else 0
    
    def add_write_latency(self, workload, value):
        self.write_latencies[self.resolve_workload(workload)].append(value)
    
    def get_write_mean(self, workload):
        idx = self.resolve_workload(workload)
        return np.mean(self.write_latencies[idx]) if self.write_latencies[idx] else 0
    
    def get_write_std(self, workload):
        idx = self.resolve_workload(workload)
        return np.std(self.write_latencies[idx]) if self.write_latencies[idx] else 0

throughputs = {"baseline": Datastore(), "distributed": Datastore()}

for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, newline='') as csvfile:
            #print(f"Processing file: {filename}")
            reader = csv.reader(csvfile, delimiter=';')
            db_type = "distributed" if "16-mb" in filename else "baseline"
            for row in reader:
                if row[Rows.PHASE.value] == "load" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value]:
                    throughputs[db_type].add_load_throughput(float(row[Rows.VALUE.value]))
                elif row[Rows.PHASE.value] == "run" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value] :
                    throughputs[db_type].add_throughput(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))
                
                if row[Rows.PHASE.value] == "run" and row[Rows.METRIC.value] == "READ" and "95" in row[Rows.MEASUREMENT.value]:
                    throughputs[db_type].add_read_latency(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))
                
                if row[Rows.PHASE.value] == "run" and (row[Rows.METRIC.value] == "INSERT" or row[Rows.METRIC.value] == "UPDATE") and "95" in row[Rows.MEASUREMENT.value]:
                    throughputs[db_type].add_write_latency(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))


def create_throughput_plot():
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
    ax.set_title('Comparison of Fjall and Distributed Database by Throughput')
    ax.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig('throughput_comparison-bs-distributed.png')  # Save the plot as a PNG file

def create_read_plot():
    workloads = ["a", "b", "c", "d"]
    db_types = ["baseline", "distributed"]
    x = np.arange(len(workloads))
    width = 0.18

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, db_type in enumerate(db_types):
        means = []
        stds = []
        ds = throughputs[db_type]
        for w in workloads:
            means.append(ds.get_read_mean(w))
            stds.append(ds.get_read_std(w))
        bar_tag = "Distributed Database" if db_type == "distributed" else "Baseline"
        bars = ax.bar(x + i * width, means, width, yerr=stds, label=f"Database: {bar_tag}")
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

    # Set x-ticks between the two bars for each workload
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(["Workload A", "Workload B", "Workload C", "Workload D"])
    ax.set_ylabel('Read Latency (ms)')
    ax.set_title('Comparison of Fjall and Distributed Database by Read Latency')
    ax.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig('read_latency_comparison-bs-distributed.png')  # Save the plot as a PNG file

def create_write_plot():
    workloads = ["a", "b", "c", "d"]
    db_types = ["baseline", "distributed"]
    x = np.arange(len(workloads))
    width = 0.18

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, db_type in enumerate(db_types):
        means = []
        stds = []
        ds = throughputs[db_type]
        for w in workloads:
            means.append(ds.get_write_mean(w))
            stds.append(ds.get_write_std(w))
        bar_tag = "Distributed Database" if db_type == "distributed" else "Baseline"
        bars = ax.bar(x + i * width, means, width, yerr=stds, label=f"Database: {bar_tag}")
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.7)

    # Set x-ticks between the two bars for each workload
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(["Workload A", "Workload B", "Workload C", "Workload D"])
    ax.set_ylabel('Write Latency (ms)')
    ax.set_title('Comparison of Fjall and Distributed Database by Write Latency')
    ax.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig('write_latency_comparison-bs-distributed.png')  # Save the plot as a PNG file

#create_throughput_plot()
create_read_plot()
create_write_plot()