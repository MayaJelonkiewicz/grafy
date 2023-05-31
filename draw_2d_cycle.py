import sys
import matplotlib.pyplot as plt
import numpy as np


points = np.loadtxt(sys.stdin)

plt.clf()
plt.plot(points[:, 0], points[:, 1])
plt.savefig("graph.png")
