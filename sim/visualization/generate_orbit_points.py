from astropy import units as u
import numpy as np

def get_orbit_path_km(orbit, num_points=200):
    # Default to 1 full orbital period
    period = orbit.period.to(u.s).value  # seconds
    times = np.linspace(0, period, num_points) * u.s

    path = []
    for t in times:
        propagated = orbit.propagate(t)
        r = propagated.r.to_value(u.km)
        path.append(r.tolist())

    return path
