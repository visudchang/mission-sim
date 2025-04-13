from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.plotting.static import StaticOrbitPlotter
import matplotlib.pyplot as plt
from poliastro.plotting import OrbitPlotter3D
from plotly.offline import plot
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