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

    orb_i_times = [i * orb_i.period / 300 for i in range(301)]
    orb_i_coords = [orb_i.propagate(t).r.to(u.km).value for t in orb_i_times]
    xi, yi, zi = zip(*orb_i_coords)

    transfer_time = hoh.get_total_time()
    transfer_times = [i * transfer_time / 180 for i in range(181)]
    transfer_coords = [orb_transfer.propagate(t).r.to(u.km).value for t in transfer_times]
    xt, yt, zt = zip(*transfer_coords)

    orb_f_times = [i * orb_f.period / 300 for i in range(301)]
    orb_f_coords = [orb_f.propagate(t).r.to(u.km).value for t in orb_f_times]
    xf, yf, zf = zip(*orb_f_coords)
    
    xs = list(xi) + list(xt) + list(xf)
    ys = list(yi) + list(yt) + list(yf)
    zs = list(zi) + list(zt) + list(zf)

    burn1_index = len(xi) - 1
    burn2_index = burn1_index + len(xt) - 1

    # Create frames (each with Earth + satellite position + trail)
    frames = []
    for i in range(len(xs)):
        marker = dict(size = 6, color = 'red')
        if i in [burn1_index, burn1_index + 1, burn1_index + 2, burn2_index, burn2_index + 1, burn2_index + 2]:
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