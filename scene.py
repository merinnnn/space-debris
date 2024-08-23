import pandas as pd
import numpy as np
from sgp4.api import Satrec
from sgp4.api import jday
from skyfield.api import Topos, load
from skyfield.sgp4lib import EarthSatellite
from model import *
from sat import Sat


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def clean_file(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()

        # Replace byte 0xa0 (non-breaking space) with a regular space
        content = content.replace(b'\xa0', b' ').replace(b'\xc9', b'E')

        with open(file_path, 'wb') as f:
            f.write(content)

    def add_object(self, obj):
        self.objects.append(obj)

    # def get_satellite_tle(norad_id):
    #     stations_url = 'https://celestrak.com/NORAD/elements/gp.php?CATNR={}'.format(norad_id)
    #     satellites = load.tle_file(stations_url)
    #     return satellites[0]
    
    # def get_current_position(satellite):
    #     ts = load.timescale()
    #     t = ts.now()

    #     geocentric = satellite.at(t)

    #     subpoint = geocentric.subpoint()
    #     return {
    #         'latitude': subpoint.latitude.degrees,
    #         'longitude': subpoint.longitude.degrees,
    #         'altitude_km': subpoint.elevation.km
    #     }

    def load(self):
        app = self.app
        add = self.add_object


        # # Load the CSV file
        # file_path = 'data\space_decay.csv'
        # data = pd.read_csv(file_path)

        # # Extract TLE data from the CSV
        # tle_lines1 = data['TLE_LINE1']
        # tle_lines2 = data['TLE_LINE2']

        # Observation time (current time or specific date)
        year, month, day, hour, minute, second = 2021, 10, 2, 12, 0, 0
        jd, fr = jday(year, month, day, hour, minute, second)

        # Calculate the position of each object using SGP4

        # for tle_line1, tle_line2 in zip(tle_lines1, tle_lines2):
        #     satellite = Satrec.twoline2rv(tle_line1, tle_line2)
        #     e, r, v = satellite.sgp4(jd, fr)
        #     if e == 0:  # If no error in the calculation
        #         add(Cube(app, pos=(r[0]/1000, r[1]/1000, r[2]/1000)))


        file_path = 'data\satellite_position.csv'
        self.clean_file(file_path)  # Remove non-breaking spaces from the CSV file


        try:
            data = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
        except UnicodeDecodeError:
            data = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')


        norad_ids = data['NORAD Number']

        satellites = [Sat(norad_id) for norad_id in norad_ids]
        for satellite in satellites:
            print (satellite.get_position_vector())
            try:
                add(Cube(app, pos=(satellite.get_position_vector())))
            except Exception as e:
                print(f"Error calculating position for NORAD ID {satellite.norad_id}: {e}")


        # for norad_id in norad_ids:
        #     satellite = EarthSatellite(get_satellite_tle(norad_id), NORAD_id)
        #     current_position = get_current_position(satellite)
        #     add(Cube(app, pos=(current_position['longitude'], current_position['latitude'], current_position['altitude_km'])))

        add(Earth(app, pos=(0, 0, 0)))

    def render(self):
        for obj in self.objects:
            obj.render()