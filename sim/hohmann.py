import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.orbits import orb0, orb1

dv = [5, 0, 0] << (u.m / u.s)
imp = Maneuver.impulse(dv)

def hohmann_plot(orb_i):
    hoh = Maneuver.hohmann(orb_i, 36000 << u.km)
    print(hoh.get_total_cost())
    print(hoh.get_total_time())

    fig, ax = plt.subplots()
    op = StaticOrbitPlotter(ax)
    orb_a, orb_f = orb_i.apply_maneuver(hoh, intermediate = True)
    op.plot(orb_i, label = "Initial orbit")
    op.plot(orb_a, label = "Transfer orbit")
    op.plot(orb_f, label = "Final orbit")

    plt.show()

def animate_hohmann_transfer(orb_i, new_radius):
    hoh = Maneuver.hohmann(orb_i, new_radius)
    orbits = orb_i.apply_maneuver(hoh, intermediate = True)
    orb_transfer = orbits[0]
    orb_f = orbits[1]

    transfer_time = hoh.get_total_time()
    minutes = 180
    times = [i * transfer_time / minutes for i in range(minutes)]
    orb_f_times = [i * 60 * u.s for i in range(2000)]
    orb_transfer_coords = [orb_transfer.propagate(t).r.to(u.km).value for t in times]
    xs, ys, zs = zip(*orb_transfer_coords)
    orb_f_coords = [orb_f.propagate(t).r.to(u.km).value for t in orb_f_times]
    xt, yt, zt = zip(*orb_f_coords)
    xs = list(xs)
    ys = list(ys)
    zs = list(zs)
    xs.extend(xt)
    ys.extend(yt)
    zs.extend(zt)

    # Create frames (each with Earth + satellite position + trail)
    frames = [
        go.Frame(
            data = [
                earth_surface,
                go.Scatter3d(
                    x = [xs[i]], y = [ys[i]], z = [zs[i]],
                    mode = 'markers',
                    marker = dict(size=6, color='red'),
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
        )
        for i in range(len(xs))
    ]

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
            title = "Animated Hohmann Transfer Orbit",
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

animate_hohmann_transfer(orb0, Earth.R + 36000 * u.km)