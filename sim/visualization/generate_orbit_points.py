from astropy import units as u
from poliastro.bodies import Earth
from poliastro.frames import Planes
from astropy.time import Time
import numpy as np

def get_orbit_path_km(orbit, num_points=120):
    # Get equally spaced time values over one orbit period
    period = orbit.period.to(u.s).value
    times = [orbit.epoch + (i * period / num_points) * u.s for i in range(num_points)]

    positions = []
    for t in times:
        r = orbit.propagate(t - orbit.epoch).r.to(u.km).value
        positions.append([float(r[0]), float(r[1]), float(r[2])])

    return positions
