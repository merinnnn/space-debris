from skyfield.api import Topos, load
from skyfield.sgp4lib import EarthSatellite
from math import radians, sin, cos


class Sat:
    def __init__(self, norad_id):
        self.norad_id = norad_id
        self.satellite = self.load_tle_data()

    def load_tle_data(self):
        stations_url = f'https://celestrak.com/NORAD/elements/gp.php?CATNR={self.norad_id}'
        satellites =load.tle_file(stations_url)
        return satellites[0]
    
    def get_position(self):
        ts = load.timescale()
        t = ts.now()
        
        geocentric = self.satellite.at(t)
        subpoint = geocentric.subpoint()

        return {
            'latitude': subpoint.latitude.degrees,
            'longitude': subpoint.longitude.degrees,
            'altitude_km': subpoint.elevation.km
            }
    
    def get_position_cartesian(self):

        position = self.get_position()

        latitude = position['latitude']
        longitude = position['longitude']
        altitude_km = position['altitude_km']

        # Convert latitude and longitude from degrees to radians
        latitude_rad = radians(latitude)
        longitude_rad = radians(longitude)

        # Earth radius in km
        EARTH_RADIUS_KM = 6371.0
        
        # Compute total radius
        radius = EARTH_RADIUS_KM + altitude_km

        # Convert to Cartesian coordinates
        x = radius * cos(latitude_rad) * cos(longitude_rad) / 1000
        y = radius * cos(latitude_rad) * sin(longitude_rad) / 1000
        z = radius * sin(latitude_rad) / 1000

        return (x, y, z)
    
    def get_position_vector(self):
        position = self.get_position()
        return (
            position['latitude'] / 100, 
            position['longitude'] / 100, 
            position['altitude_km'] / 100
            )
    
    