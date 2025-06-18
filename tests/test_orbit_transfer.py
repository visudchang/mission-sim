import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *

from datetime import datetime
from poliastro.maneuver import Maneuver
from poliastro.bodies import Earth
from sim.visualization.generate_orbit_points import get_orbit_path_km
from sim.maneuvers.hohmann import hohmann_transfer_dvs, hohmann_transfer_dv
from sim.maneuvers.inclination_change import compute_inclination_change_dv_general
from sim.maneuvers.burns import periapsis_adjustment_dv, time_to_periapsis
from astropy.time import Time
import matplotlib
from poliastro.util import wrap_angle
matplotlib.use("Agg")

mission_config = {
    "epoch": Time("2025-01-01 00:00:00", scale = "utc"),
    "attractor": Earth,
    "a": Earth.R + 4000 * u.km,
    "ecc": 0 * u.one,
    "inc": 0 * u.deg,
    "raan": 0 * u.deg,
    "argp": 0 * u.deg,
    "nu": 0 * u.deg,
    "dry_mass": 4 * u.kg,
    "prop_mass": 1 * u.kg,
    "max_thrust": 0.1 * u.N # cold gas
}

orb0 = Orbit.from_classical(cfg["attractor"],
                            cfg["a"],
                            cfg["ecc"],
                            cfg["inc"],
                            cfg["raan"],
                            cfg["argp"],
                            cfg["nu"],
                            epoch = cfg["epoch"])

def plan_orbit_transfer(periapsis_radius, apoapsis_radius):
    mu = 398600.4418  # km^3/s^2

    # Start with the current orbit
    orb = orb0

    # Periapsis radius (current orbit)
    r1 = orb.a.to_value(u.km)
    r2 = apoapsis_radius.to_value(u.km)

    # Time to periapsis
    t_periapsis = time_to_periapsis(orb).to_value(u.s)
    burn1_time = t_periapsis

    # Calculate the delta-v to raise apoapsis
    dv1, _ = hohmann_transfer_dvs(r1, r2, mu)
    v_vec = orb.v.to_value(u.km / u.s)
    unit_v = v_vec / np.linalg.norm(v_vec)
    dv_vec1 = unit_v * dv1.to_value(u.km / u.s)

    print("dv_vec1: ", dv_vec1)

    # Simulate orbit after burn 1
    maneuver1 = Maneuver.impulse(dv_vec1 * u.km / u.s)
    orb1 = orb.apply_maneuver(maneuver1)

    # Calculate time to apoapsis in the new (elliptical) orbit
    try:
        target_nu = wrap_angle(180 * u.deg)
        time_to_apoapsis = orb1.time_to_anomaly(target_nu)
        if time_to_apoapsis < 0 * u.s or abs(time_to_apoapsis.to_value(u.s)) < 1e-6:
            raise ValueError("Bad apoapsis time")
    except:
        print("[Warning] Fallback: using half-period to reach apoapsis")
        time_to_apoapsis = orb1.period / 2
    burn2_time = burn1_time + time_to_apoapsis.to_value(u.s)

    print(f"[Debug] time_to_apoapsis: {time_to_apoapsis}, burn2_time: {burn2_time}")

    # Propagate to apoapsis to get direction for second burn
    orb2 = orb1.propagate(time_to_apoapsis)
    unit_v_apo = orb2.v.to_value(u.km / u.s) / np.linalg.norm(orb2.v.to_value(u.km / u.s))

    # Burn 2: raise periapsis to target value
    rp_target = periapsis_radius.to_value(u.km)
    dv_periapsis = periapsis_adjustment_dv(rp_current=r1, rp_target=rp_target, ra_fixed=r2, mu=mu)
    dv_vec_periapsis = unit_v_apo * dv_periapsis.to_value(u.km / u.s)

    print("dv_vec_periapsis: ", dv_vec_periapsis)

    '''
    # Compute inclination change
    r_vec = orb2.r.to_value(u.km)
    v_vec_total = orb2.v.to_value(u.km / u.s) + dv_vec_periapsis

    h_vec = np.cross(r_vec, v_vec_total)
    current_inc = np.arccos(h_vec[2] / np.linalg.norm(h_vec)) * 180 / np.pi

    dv_incl = compute_inclination_change_dv_general(
        r_vec=r_vec,
        v_vec=v_vec_total,
        current_inc_deg=current_inc,
        target_inc_deg=inclination.to_value(u.deg)
    )

    dv_vec2 = dv_vec_periapsis + dv_incl
    '''

plan_orbit_transfer(9000 * u.km, 9000 * u.km)
print(hohmann_transfer_dv(orb0, 9000 * u.km))