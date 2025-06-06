from datetime import datetime
import numpy as np
from astropy import units as u
from poliastro.maneuver import Maneuver
from poliastro.bodies import Earth
from sim.visualization.generate_orbit_points import get_orbit_path_km
from astropy.time import Time
import matplotlib
matplotlib.use("Agg")

class Spacecraft:
    def __init__(self, initial_orbit, mass=500.0 * u.kg, thrust=2000.0 * u.N):
        self.initial_orbit = initial_orbit
        self.orbit = initial_orbit
        self.mass = mass
        self.thrust = thrust
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.velocity = self.orbit.v
        self.position = self.orbit.r
        self.burns = []  # list of (mission_time, delta_v_vec)
        self.history = []  # list of (event_type, value, mission_time)
        self.orbit_path = get_orbit_path_km(self.orbit)

    def apply_burn(self, delta_v_vec):
        magnitude = np.linalg.norm(delta_v_vec)
        if magnitude == 0:
            return

        # Burn happens at current mission time, not future propagation
        maneuver = Maneuver.impulse(delta_v_vec)
        self.orbit = self.orbit.apply_maneuver(maneuver)
        self.velocity = self.orbit.v
        self.position = self.orbit.r
        self.acceleration = (self.thrust / self.mass) * (delta_v_vec / magnitude)
        self.acceleration = self.acceleration.to(u.km / u.s**2)

        self.burns.append((datetime.now(), delta_v_vec))
        self.history.append(("burn", delta_v_vec, datetime.now()))
        self.orbit_path = get_orbit_path_km(self.orbit)

    def propagate(self, current_time):
        # Convert datetime to Astropy Time
        target_time = Time(current_time)

        # Recompute orbit from initial + all burns
        self.orbit = self.initial_orbit
        for _, delta_v_vec in self.burns:
            self.orbit = self.orbit.apply_maneuver(Maneuver.impulse(delta_v_vec))

        # Propagate to the new current_time
        self.orbit = self.orbit.propagate(target_time)

        # Update state vectors
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)

        print("[Spacecraft] Propagated to:", current_time.isoformat())
        print("[Spacecraft] Position (km):", self.orbit.r.to_value(u.km).tolist())

    def get_telemetry(self, include_path=False):
        telemetry = {
            "VEL": np.linalg.norm(self.velocity).to(u.km / u.s).value,
            "ALT": (np.linalg.norm(self.position) - Earth.R).to(u.km).value,
            "ACC": np.linalg.norm(self.acceleration).to(u.km / u.s**2).value,
            "timestamp": datetime.now().isoformat(),
            "position": self.position.to_value(u.km).tolist(),
            "velocity": self.velocity.to_value(u.km / u.s).tolist(),
        }
        if include_path:
            telemetry["orbitPath"] = self.get_orbit_path()
        return telemetry

    def get_orbit_path(self):
        return self.orbit_path
