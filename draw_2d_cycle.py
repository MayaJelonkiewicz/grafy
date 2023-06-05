import sys
import matplotlib.pyplot as plt
import numpy as np


points = np.loadtxt(sys.stdin)
points = np.row_stack((points, points[:1])) # close loop

plt.clf()
plt.plot(points[:, 0], points[:, 1])
plt.savefig("graph.png")
