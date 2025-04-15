import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.orbits import orb0, orb2

def compute_inclination_change_dv(orbit_initial, orbit_final):
    delta_i = abs(orbit_initial.inc - orbit_final.inc).to(u.rad).value
    r_vec = orbit_initial.r.to(u.km).value
    v_vec = orbit_initial.v.to(u.km / u.s).value

    # Node line = cross product of angular momentum vectors (axis of rotation)
    h1 = np.cross(r_vec, v_vec)
    h2 = np.cross(orbit_final.r.to(u.km).value, orbit_final.v.to(u.km / u.s).value)
    axis = np.cross(h1, h2)
    axis = axis / np.linalg.norm(axis)

    # Rotate velocity vector by delta inclination
    rot = R.from_rotvec(delta_i * axis)
    v_rotated = rot.apply(v_vec)

    dv_vec = v_rotated - v_vec
    return dv_vec * (u.km / u.s)

def animate_inclination_change_orb_f(orb_i, orb_f):
    di = abs(orb_i.inc.to(u.rad).value - orb_f.inc.to(u.rad).value)
    dv = 2 * orb_i.v.to(u.km / u.s).value * np.sin(di / 2)

    orb_i_times = [i * orb_i.period / 300 for i in range(301)]
    orb_i_coords = [orb_i.propagate(t).r.to(u.km).value for t in orb_i_times]
    xi, yi, zi = zip(*orb_i_coords)

    orb_f_times = [i * orb_f.period / 300 for i in range(301)]
    orb_f_coords = [orb_f.propagate(t).r.to(u.km).value for t in orb_f_times]
    xf, yf, zf = zip(*orb_f_coords)
    
    xs = list(xi) + list(xf)
    ys = list(yi) + list(yf)
    zs = list(zi) + list(zf)

    burn_index = len(xi) - 1

    # Create frames (each with Earth + satellite position + trail)
    frames = []
    for i in range(len(xs)):
        marker = dict(size = 6, color = 'red')
        if i in [burn_index, burn_index + 1, burn_index + 2]:
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
            title = "Animated Inclination Change orb_f",
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

    print(f"Total delta v: {np.linalg.norm(dv) * u.km / u.s}")

    fig.show()

def animate_inclination_change_dv(orb_i, dv):
    orb_i_times = [i * orb_i.period / 300 for i in range(301)]
    orb_i_coords = [orb_i.propagate(t).r.to(u.km).value for t in orb_i_times]
    xi, yi, zi = zip(*orb_i_coords)

    imp = Maneuver.impulse(dv)
    orb_f = orb_i.apply_maneuver(imp)

    orb_f_times = [i * orb_f.period / 300 for i in range(301)]
    orb_f_coords = [orb_f.propagate(t).r.to(u.km).value for t in orb_f_times]
    xf, yf, zf = zip(*orb_f_coords)
    
    xs = list(xi) + list(xf)
    ys = list(yi) + list(yf)
    zs = list(zi) + list(zf)

    burn_index = len(xi) - 1

    # Create frames (each with Earth + satellite position + trail)
    frames = []
    for i in range(len(xs)):
        marker = dict(size = 6, color = 'red')
        if i in [burn_index, burn_index + 1, burn_index + 2]:
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
            title = "Animated Inclination Change dv",
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

    print(f"Total delta v: {imp.get_total_cost()}")

    fig.show()

print(compute_inclination_change_dv(orb0, orb2))
animate_inclination_change_dv(orb0, compute_inclination_change_dv(orb0, orb2))
animate_inclination_change_orb_f(orb0, orb2)
