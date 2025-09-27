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

throughputs = [[] for _ in range(4)]
latencies = [[] for _ in range(4)]

for filename in os.listdir('.'):
    if filename.endswith('.csv'):
        with open(filename, newline='') as csvfile:
            #print(f"Processing file: {filename}")
            reader = csv.reader(csvfile, delimiter=';')
            channel_count = filename.split('-')[0]
            if channel_count == 'http':
                channel_count = 4
            else:
                channel_count = int(channel_count)
            for row in reader:
                if row[Rows.PHASE.value] == "load":
                    continue
                if row[Rows.METRIC.value] == "OVERALL" and "Throughput" in row[Rows.MEASUREMENT.value] :
                    throughputs[channel_count - 1].append(float(row[Rows.VALUE.value]))
                if row[Rows.METRIC.value] == "READ" and "AverageLatency" in row[Rows.MEASUREMENT.value]:
                    latencies[channel_count - 1].append(float(row[Rows.VALUE.value]))

def plot_http_vs_single_channel():
    http_throughputs = throughputs[3]
    single_throughputs = throughputs[0]

    avg_throughputs = [np.mean(single_throughputs), np.mean(http_throughputs)]
    std_throughputs = [np.std(single_throughputs), np.std(http_throughputs)]

    labels = ['Single Comm-Channel', 'HTTP Requests']

    plt.bar(labels, avg_throughputs, yerr=std_throughputs, capsize=10)
    plt.title('Average Throughput Comparison')
    plt.ylabel('Throughput (ops/sec)')

    plt.tight_layout()
    #plt.show()
    plt.savefig('http_vs_single_channel.png')

def compare_channels():
    avg_throughputs = [np.mean(throughputs[i]) for i in range(3)]
    std_throughputs = [np.std(throughputs[i]) for i in range(3)]

    labels = ['1 Channel', '2 Channels', '3 Channels']

    plt.figure(figsize=(6, 6))
    plt.bar(labels, avg_throughputs, yerr=std_throughputs, capsize=10)
    plt.title('Average Throughput by Comm-Channel Count')
    plt.ylabel('Throughput (ops/sec)')

    plt.tight_layout()
    #plt.show()
    plt.savefig('channel_comparison.png')

plot_http_vs_single_channel()
compare_channels()