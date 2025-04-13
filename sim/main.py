import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.orbits import orb0

time_step = 60 * u.s
duration = 60 * 60 * u.s
times = [time_step * i for i in range(int(duration / time_step))]

def live_telemetry(orbit):
    for t in times:
        propogated_orbit = orbit.propagate(t)
        r = propogated_orbit.r
        v = propogated_orbit.v
        print(f"[T + {t.to(u.min)}] Position: {r}, Velocity: {v}")
        time.sleep(1)

def show_propagation(orbit):
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

show_propagation(orb0)