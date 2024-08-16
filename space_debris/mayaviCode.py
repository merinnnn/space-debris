import pandas as pd
from mayavi import mlab
import numpy as np
from tvtk.api import tvtk
from sgp4.api import Satrec, jday


# Create a sphere to represent the Earth
def create_earth(radius=6371, texture_file='earth_texture.jpg'):
    # Generate the sphere's mesh
    phi, theta = np.mgrid[0:np.pi:100j, 0:2*np.pi:100j]
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    # Create the Earth mesh
    earth = mlab.mesh(x, y, z, representation='surface', scalars=z)
    earth.actor.actor.mapper.interpolate_scalars_before_mapping = True

    # Load the texture
    texture = tvtk.JPEGReader(file_name=texture_file)

    # Apply the texture directly to the Earth mesh
    earth.actor.enable_texture = True
    earth.actor.actor.texture = tvtk.Texture(input_connection=texture.output_port)
    
    return earth

# Function to convert TLE to position
def tle_to_position(line1, line2, jd):
    sat = Satrec.twoline2rv(line1, line2)
    e, r, v = sat.sgp4(jd[0], jd[1])
    if e == 0:
        return r  # returns position in km
    else:
        return None

# Function to plot satellite positions
def plot_satellite(position, color=(1, 0, 0)):
    x, y, z = position
    mlab.points3d(x, y, z, color=color, scale_factor=200)  # Adjust scale_factor as needed

# Plot the Earth with texture
mlab.figure(size=(800, 800))
create_earth(texture_file='space_debris/world.topo.bathy.200412x294x196.jpg')

# Load the CSV file
file_path = 'space_debris/space_decay.csv'
data = pd.read_csv(file_path)

# Extract TLE data from the CSV
tle_lines1 = data['TLE_LINE1']
tle_lines2 = data['TLE_LINE2']

# Observation time (current time or specific date)
year, month, day, hour, minute, second = 2021, 10, 2, 12, 0, 0
jd, fr = jday(year, month, day, hour, minute, second)

# Calculate the position of each object using SGP4
for tle_line1, tle_line2 in zip(tle_lines1, tle_lines2):
    satellite_position = tle_to_position(tle_line1, tle_line2, (jd, fr))
    if satellite_position:
        plot_satellite(satellite_position)

# Set the view (optional)
mlab.view(azimuth=60, elevation=45, distance=25000, focalpoint=(0, 0, 0))

# Show the visualization
mlab.show()
