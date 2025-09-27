import numpy as np


# Percentage values for different memtable configurations
data = {
    "4": [28.6, 28.5, 0.02, 44.5],
    "16": [34.4, 34.1, 0.09, 52.8],
    "32": [37, 36, 0.05, 57],
}

import matplotlib.pyplot as plt

def plot():
    workloads = ['A', 'B', 'C', 'D']
    memtable_sizes = list(data.keys())
    values = np.array([data[size] for size in memtable_sizes])

    x = np.arange(len(memtable_sizes))
    bar_width = 0.2

    fig, ax = plt.subplots()
    bars = []
    for i in range(len(workloads)):
        bar = ax.bar(x + i * bar_width, values[:, i], width=bar_width, label=f'Workload {workloads[i]}')
        bars.append(bar)

    # Add percentage values above bars
    for i in range(len(workloads)):
        for j, rect in enumerate(bars[i]):
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('Memtable Size')
    ax.set_ylabel('Percentage of Requests Answered from the DPU (%)')
    ax.set_xticks(x + 1.5 * bar_width)
    ax.set_xticklabels(memtable_sizes)
    ax.legend()
    plt.tight_layout()
    plt.savefig('percentage-memtable.png')
    #plt.show()

plot()