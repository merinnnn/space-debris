import pandas as pd
import numpy as np
from sgp4.api import Satrec
from sgp4.api import jday
from model import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object


        # Load the CSV file
        file_path = 'prototype-1\space_decay.csv'
        data = pd.read_csv(file_path)

        # Extract TLE data from the CSV
        tle_lines1 = data['TLE_LINE1']
        tle_lines2 = data['TLE_LINE2']

        # Observation time (current time or specific date)
        year, month, day, hour, minute, second = 2021, 10, 2, 12, 0, 0
        jd, fr = jday(year, month, day, hour, minute, second)

        # Calculate the position of each object using SGP4
        for tle_line1, tle_line2 in zip(tle_lines1, tle_lines2):
            satellite = Satrec.twoline2rv(tle_line1, tle_line2)
            e, r, v = satellite.sgp4(jd, fr)
            if e == 0:  # If no error in the calculation
                add(Cube(app, pos=(r[0]/1000, r[1]/1000, r[2]/1000)))

        # n, s = 30, 3
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))

        add(Earth(app, pos=(0, 0, 0)))

    def render(self):
        for obj in self.objects:
            obj.render()