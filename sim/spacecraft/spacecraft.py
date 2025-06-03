from datetime import datetime
import numpy as np
from astropy import units as u
from poliastro.maneuver import Maneuver
from poliastro.bodies import Earth
from sim.visualization.generate_orbit_points import get_orbit_path_km
import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend

class Spacecraft:
    def __init__(self, initial_orbit, mass=500.0 * u.kg, thrust=2000.0 * u.N):
        self.orbit = initial_orbit
        self.last_update = datetime.now()
        self.position = initial_orbit.r
        self.velocity = initial_orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.mass = mass
        self.thrust = thrust
        self.history = []
        self.orbit_path = get_orbit_path_km(self.orbit)

    def apply_burn(self, delta_v_vec):
        delta_v_mag = np.linalg.norm(delta_v_vec)

        # Duration = (mass * |Δv|) / thrust
        duration = (self.mass * delta_v_mag) / self.thrust

        # Acceleration = (thrust / mass) in direction of Δv
        acceleration_vector = (self.thrust / self.mass) * (delta_v_vec / delta_v_mag)

        # Apply maneuver (impulsive for now)
        maneuver = Maneuver.impulse(delta_v_vec)
        self.orbit = self.orbit.apply_maneuver(maneuver)
        self.velocity = self.orbit.v
        self.position = self.orbit.r
        self.acceleration = acceleration_vector.to(u.km / u.s**2)  # convert to km/s²

        self.orbit_path = get_orbit_path_km(self.orbit)
        self.history.append(("burn", delta_v_vec, datetime.now(), duration))

    def propagate(self, to_time):
        dt = (to_time - self.last_update).total_seconds() * u.s
        self.orbit = self.orbit.propagate(dt)
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.last_update = to_time

    def get_telemetry(self, include_path=False):
        telemetry = {
            "VEL": np.linalg.norm(self.velocity).to(u.km / u.s).value,
            "ALT": (np.linalg.norm(self.position) - Earth.R).to(u.km).value,
            "ACC": np.linalg.norm(self.acceleration).to(u.km / u.s**2).value,
            "timestamp": datetime.now().isoformat(),
            "position": self.position.to_value(u.km).tolist(),
            "velocity": self.velocity.to_value(u.km / u.s).tolist(),
            "orbitPath": get_orbit_path_km(self.orbit)
        }
        if include_path:
            telemetry["orbitPath"] = self.get_orbit_path()

        return telemetry

    def get_orbit_path(self):
        return self.orbit_path
