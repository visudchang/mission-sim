from astropy import units as u
from poliastro.bodies import Earth
from astropy.time import Time

# CubeSat mission parameters
mission_config = {
    "epoch": Time("2025-01-01 00:00:00", scale = "utc"),
    "attractor": Earth,
    "a": Earth.R + 500 * u.km,
    "ecc": 0 * u.one,
    "inc": 0 * u.deg,
    "raan": 0 * u.deg,
    "argp": 0 * u.deg,
    "nu": 0 * u.deg,
    "dry_mass": 4 * u.kg,
    "prop_mass": 1 * u.kg,
    "max_thrust": 0.1 * u.N # cold gas
}