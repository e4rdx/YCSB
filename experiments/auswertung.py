import matplotlib.pyplot as plt
import numpy as np
import csv

baseline = [0, 0, 0, 0]
dma_copy = [0, 0, 0, 0]

baseline_update = [0, 0, 0, 0]
dma_copy_update = [0, 0, 0, 0]

baseline_read = [0, 0, 0, 0]
dma_copy_read = [0, 0, 0, 0]

with open('experiment-results.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        print(', '.join(row))
        if row[3] == "OVERALL" and "Throughput" in row[4]:
            idx = 0 if row[1] == "a" else 2
            idx += 0 if row[2] == "load" else 1
            if row[0] == 'baseline':
                baseline[idx] = int(float(row[5]))
            elif row[0] == 'dma_copy':
                dma_copy[idx] = int(float(row[5]))
        
        if (row[3] == "UPDATE" or row[3] == "INSERT") and "Average" in row[4]:
            idx = 0 if row[1] == "a" else 2
            idx += 0 if row[2] == "load" else 1
            if row[0] == 'baseline':
                baseline_update[idx] = int(float(row[5]))
            elif row[0] == 'dma_copy':
                dma_copy_update[idx] = int(float(row[5]))

        if row[3] == "READ" and "Average" in row[4]:
            idx = 0 if row[1] == "a" else 2
            idx += 0 if row[2] == "load" else 1
            if row[0] == 'baseline':
                baseline_read[idx] = int(float(row[5]))
            elif row[0] == 'dma_copy':
                dma_copy_read[idx] = int(float(row[5]))

def plot_results(baseline, dma_copy, ylabel):
    benchmarks = ("A Load", "A Run", "B Load", "B Run")
    data = {
        'Baseline': baseline,
        'DMA-Copy': dma_copy,
    }

    x = np.arange(len(benchmarks))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in data.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel(ylabel)
    ax.set_title('Benchmark Results')
    ax.set_xticks(x + width, benchmarks)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, max(max(baseline), max(dma_copy)) * 1.3)

    plt.show()

plot_results(baseline, dma_copy, 'Throughput(ops/sec)')

plot_results(baseline_update, dma_copy_update, 'Average Insert Latency(us)')

plot_results(baseline_read, dma_copy_read, 'Average Read Latency(us)')