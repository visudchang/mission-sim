import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
# from poliastro.plotting.static import StaticOrbitPlotter
import matplotlib.pyplot as plt
from poliastro.plotting import OrbitPlotter3D, OrbitPlotter2D
from plotly.offline import plot
import plotly.graph_objects as go
import time
from sim.config import mission_config as cfg
from astropy.time import Time
from sim.visualization.generate_earth import earth_surface
from poliastro.maneuver import Maneuver
from scipy.spatial.transform import Rotation as R
from dataclasses import dataclass

