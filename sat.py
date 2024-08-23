from skyfield.api import Topos, load
from skyfield.sgp4lib import EarthSatellite

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
    
    def get_position_vector(self):
        position = self.get_position()
        return (
            position['latitude'] / 100, 
            position['longitude'] / 100, 
            position['altitude_km'] / 100
            )
    
    