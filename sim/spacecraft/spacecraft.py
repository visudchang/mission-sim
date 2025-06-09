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
        self.mission_start = datetime.now()

    def apply_burn(self, delta_v_vec):
        magnitude = np.linalg.norm(delta_v_vec)
        if magnitude == 0:
            return

        # Compute relative mission time in seconds
        mission_time = (datetime.now() - self.mission_start).total_seconds() * u.s
        self.burns.append((mission_time, delta_v_vec))
        self.history.append(("burn", delta_v_vec, mission_time))
        print(f"[Spacecraft] Logged burn at T+{mission_time:.2f}: Δv = {delta_v_vec}")

    def propagate(self, mission_time_seconds):
        mission_time = mission_time_seconds * u.s
        print(f"\n[Spacecraft] Propagating to T+{mission_time:.2f}")

        # Reset to initial orbit before reapplying burns
        self.orbit = self.initial_orbit

        if not self.burns:
            print("[Spacecraft] No burns recorded.")
        else:
            print(f"[Spacecraft] {len(self.burns)} burn(s) on record:")
            for i, (burn_time, delta_v_vec) in enumerate(self.burns):
                print(f"  Burn {i}: T+{burn_time:.2f}, Δv = {delta_v_vec}")

        # Apply burns that should have occurred by this time
        for burn_time, delta_v_vec in self.burns:
            if burn_time < mission_time:
                print(f"  ➤ Applying burn at T+{burn_time:.2f}")
                self.orbit = self.orbit.apply_maneuver(Maneuver.impulse(delta_v_vec))
            else:
                print(f"  ✘ Skipping burn at T+{burn_time:.2f} (in the future)")

        self.orbit = self.orbit.propagate(mission_time)
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)

        print("[Spacecraft] Final position (km):", self.orbit.r.to_value(u.km))
        print("[Spacecraft] Final velocity (km/s):", self.orbit.v.to_value(u.km / u.s))


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
