import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *

# Initial orbit
epoch = Time("2025-01-01 00:00:00", scale="utc")
orbit = Orbit.from_classical(Earth,
                             Earth.R + 500 * u.km,
                             0.0 * u.one,
                             53 * u.deg,
                             0 * u.deg,
                             0 * u.deg,
                             0 * u.deg,
                             epoch=epoch)

# Propagate orbit and collect positions
times = [i * 60 * u.s for i in range(61)]  # 60 minutes
coords = [orbit.propagate(t).r.to(u.km).value for t in times]
xs, ys, zs = zip(*coords)

# Create frames (each with Earth + satellite position + trail)
frames = [
    go.Frame(
        data=[
            earth_surface,
            go.Scatter3d(
                x=[xs[i]], y=[ys[i]], z=[zs[i]],
                mode='markers',
                marker=dict(size=6, color='red'),
                name='Satellite'
            ),
            go.Scatter3d(
                x=xs[:i+1], y=ys[:i+1], z=zs[:i+1],
                mode='lines',
                line=dict(width=2, color='white'),
                name='Orbit Path'
            )
        ],
        name=f'frame{i}'
    )
    for i in range(len(xs))
]

# Base figure
fig = go.Figure(
    data=[
        earth_surface,
        go.Scatter3d(x=[xs[0]], y=[ys[0]], z=[zs[0]],
                     mode='markers', marker=dict(size=6, color='red')),
        go.Scatter3d(x=[], y=[], z=[], mode='lines',
                     line=dict(width=2, color='white'))
    ],
    layout=go.Layout(
        title="Animated CubeSat Orbit Around Earth",
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Z (km)',
            aspectmode='data'
        ),
        updatemenus=[dict(
            type='buttons',
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, {
                              'frame': {'duration': 100, 'redraw': True},
                              'fromcurrent': True,
                              'mode': 'immediate'}])],
            showactive=False
        )]
    ),
    frames=frames
)

fig.show()
