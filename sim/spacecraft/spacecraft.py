from datetime import datetime
import numpy as np
from astropy import units as u
from poliastro.maneuver import Maneuver
from poliastro.bodies import Earth
from sim.visualization.generate_orbit_points import get_orbit_path_km
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend

class Spacecraft:
    def __init__(self, initial_orbit):
        self.orbit = initial_orbit
        self.last_update = datetime.now()
        self.position = initial_orbit.r
        self.velocity = initial_orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.history = []

    def propagate(self, to_time):
        dt = (to_time - self.last_update).total_seconds() * u.s
        self.orbit = self.orbit.propagate(dt)
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.last_update = to_time

    def apply_burn(self, delta_v_vec):
        maneuver = Maneuver.impulse(delta_v_vec)
        self.orbit = self.orbit.apply_maneuver(maneuver)
        self.velocity = self.orbit.v
        self.position = self.orbit.r
        self.acceleration = delta_v_vec / 1.0 * (u.km / u.s**2)
        self.history.append(("burn", delta_v_vec, datetime.now()))

    def get_telemetry(self):
        return {
            "VEL": np.linalg.norm(self.velocity).to(u.km / u.s).value,
            "ALT": (np.linalg.norm(self.position) - Earth.R).to(u.km).value,
            "ACC": np.linalg.norm(self.acceleration).to(u.km / u.s**2).value,
            "timestamp": datetime.now().isoformat(),
            "position": self.position.to_value(u.km).tolist(),
            "velocity": self.velocity.to_value(u.km / u.s).tolist(),
            "orbitPath": get_orbit_path_km(self.orbit)
        }

    def get_orbit_path(self):
        return get_orbit_path_km(self.orbit)
