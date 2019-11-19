#! /usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt


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

plt.hist(data_trimmed, bins = 'auto')
plt.xlabel("Number of Mismatches")
plt.ylabel("Occurrences")
plt.show()

#np.histogram(data_trimmed, bins = 10)
#plt.show()
