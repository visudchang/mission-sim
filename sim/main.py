import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.orbits import orb0
from sim.propagation import show_propagation
from sim.animated_orbit import animate_orbit

# Select orbit
orbit = orb0

show_propagation(orbit)
animate_orbit(orbit)
