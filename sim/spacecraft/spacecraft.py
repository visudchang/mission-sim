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
        self.mission_time = 0.0 * u.s

    def apply_burn(self, delta_v_vec, mission_time_seconds=None):
        if np.linalg.norm(delta_v_vec) == 0:
            return

        mission_time = self.mission_time if mission_time_seconds is None else mission_time_seconds * u.s

        print(f"[Spacecraft] Applying immediate burn at T+{mission_time:.2f}")

        self.orbit = self.orbit.apply_maneuver(Maneuver.impulse(delta_v_vec))
        self.velocity = self.orbit.v
        self.position = self.orbit.r

        self.burns.append((mission_time, delta_v_vec))
        self.history.append(("burn", delta_v_vec, mission_time))

    def propagate(self, mission_time_seconds):
        mission_time = mission_time_seconds * u.s
        
        # Always propagate from current state
        dt = mission_time - self.mission_time
        if dt <= 0 * u.s:
            print(f"[Spacecraft] Already at T+{self.mission_time:.2f}")
            return

        print(f"[Spacecraft] Advancing by {dt:.2f}")
        self.orbit = self.orbit.propagate(dt)
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.mission_time = mission_time

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
