import pandas as pd
import numpy as np

class Satel:
    earth_radius_km = 6371  # Radius of Earth in kilometers

    def __init__(self, name, perigee_km, apogee_km, eccentricity, inclination_deg):
        self.name = name
        self.perigee_km = self.convert_to_float(perigee_km)
        self.apogee_km = self.convert_to_float(apogee_km)
        self.eccentricity = float(eccentricity)
        self.inclination_deg = self.convert_to_float(inclination_deg)
        self.inclination_rad = np.deg2rad(self.inclination_deg)
        self.semi_major_axis_km = (self.perigee_km + self.apogee_km + 2 * self.earth_radius_km) / 2

    @staticmethod
    def convert_to_float(value):
        """Convert a comma-separated string to a float, with error handling."""
        try:
            print(1)
            return float(value.replace(',', ''))
        except ValueError:
            raise ValueError(f"Cannot convert to float: {value}")

    def calculate_coordinates(self, true_anomaly_deg=0):
        """Calculates the satellite's Cartesian coordinates in the ECI frame."""
        true_anomaly_rad = np.deg2rad(true_anomaly_deg)
        r_km = self.semi_major_axis_km * (1 - self.eccentricity**2) / (1 + self.eccentricity * np.cos(true_anomaly_rad))

        x_orbital_km = r_km * np.cos(true_anomaly_rad)
        y_orbital_km = r_km * np.sin(true_anomaly_rad)
        z_orbital_km = 0  # Assuming 2D orbit for simplicity

        x_eci_km = x_orbital_km
        y_eci_km = y_orbital_km * np.cos(self.inclination_rad)
        z_eci_km = y_orbital_km * np.sin(self.inclination_rad)

        return x_eci_km, y_eci_km, z_eci_km

    def __str__(self):
        coordinates = self.calculate_coordinates()
        return f"Satellite: {self.name}\nCoordinates (x, y, z) in km: {coordinates}"


