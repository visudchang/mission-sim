from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.plotting.static import StaticOrbitPlotter
import matplotlib.pyplot as plt
from poliastro.plotting import OrbitPlotter3D
from plotly.offline import plot
import plotly.graph_objects as go
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.config import mission_config as cfg

orbit = Orbit.from_classical(
    cfg["attractor"],
    cfg["a"],
    cfg["ecc"],
    cfg["inc"],
    cfg["raan"],
    cfg["argp"],
    cfg["nu"],
    epoch = cfg["epoch"]
)

time_step = 60 * u.s
duration = 30 * 60 * u.s
times = [time_step * i for i in range(int(duration / time_step))]

def live_telemetry():
    for t in times:
        propogated_orbit = orbit.propagate(t)
        r = propogated_orbit.r
        v = propogated_orbit.v
        print(f"[T + {t.to(u.min)}] Position: {r}, Velocity: {v}")
        time.sleep(1)

coords = [orbit.propagate(t).r.to(u.km).value for t in times]
xs, ys, zs = zip(*coords)

fig = go.Figure(data = go.Scatter3d(
    x = xs, y = ys, z = zs,
    mode = 'lines+markers',
    marker = dict(size = 4),
    line = dict(width = 2)
))

fig.update_layout(
    title = "Orbit Propagation",
)

fig.show()