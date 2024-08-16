import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sgp4.api import Satrec
from sgp4.api import jday


# Load the CSV file
file_path = 'space_debris\space_decay.csv'
data = pd.read_csv(file_path)

# Extract TLE data from the CSV
tle_lines1 = data['TLE_LINE1']
tle_lines2 = data['TLE_LINE2']

# Initialize arrays to store positions
x_positions = []
y_positions = []
z_positions = []

# Observation time (current time or specific date)
year, month, day, hour, minute, second = 2021, 10, 2, 12, 0, 0
jd, fr = jday(year, month, day, hour, minute, second)

# Calculate the position of each object using SGP4
for tle_line1, tle_line2 in zip(tle_lines1, tle_lines2):
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    e, r, v = satellite.sgp4(jd, fr)
    if e == 0:  # If no error in the calculation
        x_positions.append(r[0])
        y_positions.append(r[1])
        z_positions.append(r[2])

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot the Earth as a sphere
earth_radius = 6371  # Earth's radius in kilometers
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the Earth
ax.plot_surface(x_earth, y_earth, z_earth, color='blue', alpha=0.3)

# Plot the debris objects
ax.scatter(x_positions, y_positions, z_positions, color='red')

# Remove the axes
ax.set_axis_off()

# Set aspect ratio to be equal, so the Earth looks like a sphere
ax.set_box_aspect([1, 1, 1])

plt.show()
