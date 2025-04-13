from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.plotting.static import StaticOrbitPlotter
import matplotlib.pyplot as plt
from poliastro.plotting import OrbitPlotter3D
from plotly.offline import plot
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.config import mission_config as cfg

orb0 = Orbit.from_classical(
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


fig, ax = plt.subplots(figsize=(6, 6))
plotter = StaticOrbitPlotter(ax)
plotter.plot(orb0, label="LEO Orbit")
plt.show()