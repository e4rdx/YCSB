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
        self.workloads = {"a": 1, "b": 2}
    
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

throughputs = {}
max_thread_count = 0

for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, newline='') as csvfile:
            #print(f"Processing file: {filename}")
            thread_count = filename.split('-')[0]
            max_thread_count = max(max_thread_count, int(thread_count))
            reader = csv.reader(csvfile, delimiter=';')
            if thread_count not in throughputs:
                throughputs[thread_count] = Datastore()
            for row in reader:
                if row[Rows.SERVICE.value] == "baseline":
                    continue
                if row[Rows.PHASE.value] == "load" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value]:
                    throughputs[thread_count].add_load_throughput(float(row[Rows.VALUE.value]))
                elif row[Rows.PHASE.value] == "run" and row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value]:
                    throughputs[thread_count].add_throughput(row[Rows.WORKLOAD.value], float(row[Rows.VALUE.value]))


def create_plot():
    thread_counts = sorted(int(tc) for tc in throughputs.keys())
    a_means = [throughputs[str(tc)].get_mean("a") for tc in thread_counts]
    a_stds = [throughputs[str(tc)].get_std("a") for tc in thread_counts]
    b_means = [throughputs[str(tc)].get_mean("b") for tc in thread_counts]
    b_stds = [throughputs[str(tc)].get_std("b") for tc in thread_counts]

    plt.figure(figsize=(8, 5))
    plt.errorbar(thread_counts, a_means, yerr=a_stds, marker='x', label='Workload A', capsize=4)
    plt.errorbar(thread_counts, b_means, yerr=b_stds, marker='x', label='Workload B', capsize=4)
    plt.xlabel('Thread Count')
    plt.ylabel('Throughput')
    plt.title('Throughput vs Thread Count')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    plt.savefig('throughput_thread_count.png')

create_plot()