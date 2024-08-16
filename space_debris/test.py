from sgp4.api import Satrec
from sgp4.api import jday

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
