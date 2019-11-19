
from matplotlib import pyplot as plt


def readFile(filepath):
    f = open(filepath)
    lines = []
    for line in f:
        lines.append(line)
    return lines




filepath = ''

data = readFile(filepath)

[int(i, base=16) for i in data]

plt.hist(data)
plt.show()