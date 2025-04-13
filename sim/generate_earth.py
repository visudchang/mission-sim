import numpy as np
from astropy import units as u
from poliastro.bodies import Earth
import plotly.graph_objects as go

earth_radius = Earth.R.to(u.km).value
u_vals = np.linspace(0, 2 * np.pi, 50)
v_vals = np.linspace(0, np.pi, 50)
x_sphere = earth_radius * np.outer(np.cos(u_vals), np.sin(v_vals))
y_sphere = earth_radius * np.outer(np.sin(u_vals), np.sin(v_vals))
z_sphere = earth_radius * np.outer(np.ones_like(u_vals), np.cos(v_vals))

earth_surface = go.Surface(
    x=x_sphere, y=y_sphere, z=z_sphere,
    colorscale='Blues',
    opacity=0.7,
    showscale=False
)