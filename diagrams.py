#! /usr/bin/env python3

from matplotlib import pyplot as plt
import numpy as np

def readFile(filepath):
    f = open(filepath)
    lines = []
    for line in f:
        lines.append(line)
    return lines




filepath = 'D_Coh_Results.txt'

data = readFile(filepath)

data_trimmed = []

for each in data:
    data_trimmed.append(each.split('\n',1)[0])

data_trimmed = [int(i) for i in data_trimmed]

print(data_trimmed)

bins = np.arange(9)-0.5

plt.hist(data_trimmed, bins)
plt.title("nv = 7")
plt.xticks(range(8))
plt.xlabel("Number of Mismatches")
plt.ylabel("Occurrences")
plt.show()

