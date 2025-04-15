import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.visualization.animated_orbit import animate_orbit
from sim.hohmann import animate_hohmann_transfer, hohmann_plot
from sim.inclination_change import animate_inclination_change_dv, animate_inclination_change_orb_f
from sim.orbits import orb0, orb2

def calculate_burn_plan(orb_i, orb_target):
    if orb_i.a.to(u.km).value != orb_target.a.to(u.km).value:
        animate_hohmann_transfer
    if orb_i.inc.to(u.deg).value != orb_target.inc.to(u.deg).value:
        animate_inclination_change_orb_f
    