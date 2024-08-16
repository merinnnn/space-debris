import csv

from sgp4.api import Satrec
from sgp4.api import jday

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


# Example TLE data
tle_line1 = "1 26741U 92072J   21304.94919376  .00000883  00000-0  24341-1 0  9992"
tle_line2 = "2 25544  51.6435 324.2024 0007223  13.8584  64.2474 15.48910339303824"

# Create a satellite object
satellite = Satrec.twoline2rv(tle_line1, tle_line2)

# Specify the observation time
year, month, day, hour, minute, second = 2021, 10, 2, 12, 0, 0
jd, fr = jday(year, month, day, hour, minute, second)

# Compute the position and velocity
e, r, v = satellite.sgp4(jd, fr)

# r contains the position in kilometers [x, y, z]
print(f"Position (km): {r}")



# ax = plt.axes(projection="3d")

# Create a 3D scatter plot
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')


# Plot the Earth as a sphere
earth_radius = 6371  # Earth's radius in kilometers

# Create data for a sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the Earth
ax.plot_surface(x_earth, y_earth, z_earth, color='blue', alpha=0.3)


ax.scatter(r[0], r[1], r[2])
# ax.set_axis_off()


ax.set_box_aspect([1, 1, 1])


plt.show()


# with open('space_debris\space_decay.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))