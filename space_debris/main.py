import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


# ax = plt.axes(projection="3d")
# ax.scatter(3,5,7)
# plt.show()


with open('space_debris\space_decay.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print(', '.join(row))