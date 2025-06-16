import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sim.common_imports import *

from datetime import datetime
from poliastro.maneuver import Maneuver
from poliastro.bodies import Earth
from sim.visualization.generate_orbit_points import get_orbit_path_km
from sim.maneuvers.hohmann import hohmann_transfer_dvs
from sim.maneuvers.inclination_change import compute_inclination_change_dv_general
from sim.maneuvers.burns import periapsis_adjustment_dv, time_to_periapsis
from astropy.time import Time
from tests.test_orbital_energy_cpp import compute_orbital_energy
import matplotlib
matplotlib.use("Agg")

class Spacecraft:
    def __init__(self, initial_orbit, mass=500.0 * u.kg, thrust=2000.0 * u.N):
        self.initial_orbit = initial_orbit
        self.orbit = initial_orbit
        self.mass = mass
        self.thrust = thrust
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.initial_position = self.initial_orbit.r.copy()
        self.initial_velocity = self.initial_orbit.v.copy()
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.burns = []  # list of (mission_time, delta_v_vec)
        self.burn_queue = []
        self.history = []  # list of (event_type, value, mission_time)
        self.planned_burns = []
        self.orbit_path = get_orbit_path_km(self.orbit)
        self.initial_orbit_path = self.orbit_path.copy()
        self.epoch = Time("2025-01-01T00:00:00", format="isot")
        self.mission_time = 0.0 * u.s
        self.battery = self.Battery(parent = self)
        self.mission_log = []

    class Battery:
        def __init__(self, parent, initial_percent=100.0, recharge_rate_per_sec=0.001, dv_cost_per_kms=15.0):
            self.parent = parent
            self.percent = initial_percent
            self.recharge_rate = recharge_rate_per_sec  # % per simulated second
            self.dv_cost_per_kms = dv_cost_per_kms      # % per km/s of burn

        def update(self, dt_simulated):
            self.percent = min(100.0, self.percent + self.recharge_rate * dt_simulated)

        def execute_burn(self, dv_vector_kms):
            dv_magnitude = np.linalg.norm(dv_vector_kms)
            drop = dv_magnitude * self.dv_cost_per_kms
            new_percent = self.percent - drop.to_value(u.km / u.s)
            if new_percent < 0.0:
                return False
            self.percent = new_percent
            if new_percent < 20.0:
                self.parent.log_event("Warning: Battery below 20%")
            return True

        def is_empty(self):
            return self.percent <= 0.0

        def __str__(self):
            return f"Battery: {self.percent:.2f}%"


    def apply_burn(self, delta_v_vec, mission_time_seconds=None):
        if np.linalg.norm(delta_v_vec) == 0:
            return

        mission_time = self.mission_time if mission_time_seconds is None else mission_time_seconds * u.s

        if not self.battery.execute_burn(delta_v_vec):
            print("[Spacecraft] Not enough battery available to execute burn")
            return
        
        self.orbit = self.orbit.apply_maneuver(Maneuver.impulse(delta_v_vec))
        self.velocity = self.orbit.v
        self.position = self.orbit.r

        self.burns.append((mission_time, delta_v_vec))
        self.history.append(("burn", delta_v_vec, mission_time))

        print(f"[Spacecraft] Applying immediate burn at T+{mission_time:.2f}")
        dv_mag = np.linalg.norm(delta_v_vec).to(u.km / u.s).value
        self.log_event(f"Executed burn: Δv = {dv_mag:.1f} km/s")


    def queue_burn(self, delta_v_vec, mission_time_seconds):
        self.burn_queue.append((mission_time_seconds, delta_v_vec))
        print(f"[Spacecraft] Queued burn at T+{mission_time_seconds:.2f}s: Δv = {delta_v_vec}")

    def check_burn_queue(self):
        current_time = self.mission_time.to_value(u.s)
        while self.burn_queue and self.burn_queue[0][0] <= current_time:
            mission_time_seconds, delta_v_vec = self.burn_queue.pop(0)
            self.apply_burn(delta_v_vec, mission_time_seconds)

    def propagate(self, mission_time_seconds):
        mission_time = mission_time_seconds * u.s
        
        # Always propagate from current state
        dt = mission_time - self.mission_time
        if dt <= 0 * u.s:
            # print(f"[Spacecraft] Already at T+{self.mission_time:.2f}")
            return

        # print(f"[Spacecraft] Advancing by {dt:.2f}")
        self.orbit = self.orbit.propagate(dt)
        self.position = self.orbit.r
        self.velocity = self.orbit.v
        self.acceleration = np.zeros(3) * (u.km / u.s**2)
        self.mission_time = mission_time
        self.battery.update(dt.to_value(u.s))
        self.check_burn_queue()
        # print("Before:", self.burn_queue)
        self.burn_queue = [burn for burn in self.burn_queue if burn[0] > self.mission_time.to_value(u.s) + 0.01]
        # print("After", self.burn_queue)

    def get_telemetry(self, include_path=False):
        r = np.linalg.norm(self.position.to_value(u.m))
        v = np.linalg.norm(self.velocity.to_value(u.m / u.s))
        orbital_energy = compute_orbital_energy(r, v)

        telemetry = {
            "VEL": np.linalg.norm(self.velocity).to(u.km / u.s).value,
            "ALT": (np.linalg.norm(self.position) - Earth.R).to(u.km).value,
            "ACC": np.linalg.norm(self.acceleration).to(u.km / u.s**2).value,
            "timestamp": datetime.now().isoformat(),
            "position": self.position.to_value(u.km).tolist(),
            "velocity": self.velocity.to_value(u.km / u.s).tolist(),
            "orbital_energy": orbital_energy / 1e6,
            "missionTime": self.mission_time.to_value(u.s),
            "BAT": round(self.battery.percent, 2)
        }
        if include_path:
            telemetry["orbitPath"] = self.get_orbit_path()
        return telemetry

    def get_orbit_path(self):
        return self.orbit_path

    def plan_orbit_transfer(self, periapsis_radius, apoapsis_radius, inclination):
        mu = 398600.4418
        orb = Orbit.from_vectors(Earth, self.position, self.velocity, epoch=self.epoch + self.mission_time.to(u.s))

        t_periapsis = time_to_periapsis(orb).to_value(u.s)
        burn1_time = self.mission_time.to_value(u.s) + t_periapsis

        r1 = orb.r_p.to_value(u.km) #??? this is where i suspect the error is
        r2 = apoapsis_radius.to_value(u.km)
        dv1, _ = hohmann_transfer_dvs(r1, r2, mu)

        v_vec = self.velocity.to_value(u.km / u.s)
        unit_v = v_vec / np.linalg.norm(v_vec)
        dv_vec1 = unit_v * dv1.to_value(u.km / u.s)

        self.queue_burn(dv_vec1 * u.km / u.s, mission_time_seconds=burn1_time)
        print(f"[Set Orbit] Queued burn 1 at periapsis (T+{t_periapsis:.1f}s): Δv = {dv_vec1}")

        # Wait until apoapsis
        a_transfer = (r1 + r2) / 2
        T_half = np.pi * np.sqrt(a_transfer**3 / mu) * u.s
        burn2_time = burn1_time + T_half.to_value(u.s)
        
        rp_target = periapsis_radius.to_value(u.km)
        dv_periapsis = periapsis_adjustment_dv(rp_current=r1, rp_target=rp_target, ra_fixed=r2, mu=mu)
        dv_vec_periapsis = unit_v * dv_periapsis.to_value(u.km / u.s)
        
        # Inclination change at apoapsis
        v_after_burn = v_vec + dv_vec1 + dv_vec_periapsis
        r_vec = self.position.to_value(u.km)
        h_vec = np.cross(r_vec, v_after_burn)
        current_inc = np.arccos(h_vec[2] / np.linalg.norm(h_vec)) * 180 / np.pi
        
        dv_incl = compute_inclination_change_dv_general(
            r_vec=r_vec,
            v_vec=v_after_burn,
            current_inc_deg=current_inc,
            target_inc_deg=inclination.to_value(u.deg)
        )
        
        dv_vec2 = dv_vec_periapsis + dv_incl

        self.queue_burn(dv_vec2 * u.km / u.s, mission_time_seconds=burn2_time)
        print(f"[Set Orbit] Queued burn 2 at apoapsis (T+{burn2_time - self.mission_time.to_value(u.s):.1f}s): Δv = {dv_vec2}")

        self.planned_burns = [
            {"delta_v": dv_vec1, "time": burn1_time},
            {"delta_v": dv_vec2, "time": burn2_time}
        ]
        print("Burns queued")
        a = (apoapsis_radius + periapsis_radius) / 2
        e = (apoapsis_radius - periapsis_radius) / (apoapsis_radius + periapsis_radius)
        self.log_event(f"Set Orbit: Semi-major axis: {a} | Eccentricity: {e:.4f} | Inclination: {inclination}")

    def get_planned_burns(self):
        return self.planned_burns
    
    def log_event(self, message):
        timestamp = self.mission_time.to_value(u.s)
        mins = int(timestamp // 60)
        secs = int(timestamp % 60)
        formatted_time = f"T+{mins:02}:{secs:02}"
        self.mission_log.insert(0, f"{formatted_time} — {message}")

    def reset(self):
        print("[Spacecraft] Resetting mission state...")
        
        for i in range(5):
            self.orbit = Orbit.from_vectors(Earth, self.initial_position, self.initial_velocity, epoch=self.epoch)
            self.position = self.orbit.r
            self.velocity = self.orbit.v
            self.mission_time = 0 * u.s
        self.history = []
        self.burns = []
        self.burn_queue = []
        self.planned_burns = []
        self.orbit_path = []
        self.battery.percent = 100.0
        self.log_event("Mission reset")
