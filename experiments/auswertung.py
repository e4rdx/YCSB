import matplotlib.pyplot as plt
import numpy as np
import csv

baseline = [0, 0, 0, 0]
dma_copy = [0, 0, 0, 0]

with open('experiment-results.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        print(', '.join(row))
        if row[0] == 'baseline' and row[3] == "OVERALL":
            if row[1] == "a":
                if row[2] == "load":
                    baseline[0] = int(float(row[5]))
                else:
                    baseline[1] = int(float(row[5]))
            else:
                if row[2] == "load":
                    baseline[2] = int(float(row[5]))
                else:
                    baseline[3] = int(float(row[5]))
        elif row[0] == 'dma_copy' and row[3] == "OVERALL":
            if row[1] == "a":
                if row[2] == "load":
                    dma_copy[0] = int(float(row[5]))
                else:
                    dma_copy[1] = int(float(row[5]))
            else:
                if row[2] == "load":
                    dma_copy[2] = int(float(row[5]))
                else:
                    dma_copy[3] = int(float(row[5]))

benchmarks = ("A Load", "A Run", "B Load", "B Run")
data = {
    'Baseline': baseline,
    'DMA-Copy': dma_copy,
}

x = np.arange(len(benchmarks))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Throughput(ops/sec)')
ax.set_title('Benchmark Results')
ax.set_xticks(x + width, benchmarks)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 30000)

plt.show()