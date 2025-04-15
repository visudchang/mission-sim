import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sim.common_imports import *
from sim.visualization.animated_orbit import animate_orbit
from sim.maneuvers.hohmann import animate_hohmann_transfer, hohmann_plot
from sim.maneuvers.inclination_change import animate_inclination_change_dv, animate_inclination_change_orb_f, compute_inclination_change_dv
from sim.orbits import orb0, orb2

def generate_trajectory_segments(plan, steps_per_orbit = 300):
    coords = []
    burn_indices = []

    for step in plan:
        times = [i * step.duration / steps_per_orbit for i in range(steps_per_orbit + 1)]
        segment = [step.orbit.propagate(t).r.to(u.km).value for t in times]

        if step.burn:
            burn_indices.append(len(coords) - 1)

        coords.extend(segment)
    
    return coords, burn_indices

def animate_burn_plan(coords, burn_indices):
    xs, ys, zs = zip(*coords)
    frames = []
    for i in range(len(xs)):
        marker = dict(size = 6, color = 'red')
        if i in burn_indices or i in [b + 1 for b in burn_indices] or i in [b + 2 for b in burn_indices]:
            marker = dict(size = 12, color = 'orange')
        frames.append(go.Frame(
            data = [
                earth_surface,
                go.Scatter3d(
                    x = [xs[i]], y = [ys[i]], z = [zs[i]],
                    mode = 'markers',
                    marker = marker,
                    name = 'Satellite'
                ),
                go.Scatter3d(
                    x = xs[:i+1], y = ys[:i+1], z = zs[:i+1],
                    mode = 'lines',
                    line = dict(width = 2, color = 'white'),
                    name = 'Orbit Path'
                )
            ],
            name = f'frame{i}'
        ))

    # Base figure
    fig = go.Figure(
        data = [
            earth_surface,
            go.Scatter3d(x = [xs[0]], y = [ys[0]], z = [zs[0]],
                        mode = 'markers', marker = dict(size = 6, color = 'red')),
            go.Scatter3d(x = [], y = [], z = [], mode = 'lines',
                        line = dict(width = 2, color = 'white'))
        ],
        layout=go.Layout(
            title = "Mission Burn Plan Animation",
            scene = dict(
                xaxis_title = 'X (km)',
                yaxis_title = 'Y (km)',
                zaxis_title = 'Z (km)',
                aspectmode = 'data'
            ),
            updatemenus = [dict(
                type = 'buttons',
                buttons = [dict(label = 'Play',
                            method = 'animate',
                            args = [None, {
                                'frame': {'duration': 25, 'redraw': True},
                                'fromcurrent': True,
                                'mode': 'immediate'}])],
                showactive = False
            )]
        ),
        frames = frames
    )

    fig.show()