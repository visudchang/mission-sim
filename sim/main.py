import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.orbits import orb0, orb2, orb3
from sim.propagation.propagation import show_propagation,show_flight_plan_propagation
from sim.visualization.animated_orbit import animate_orbit
from sim.maneuvers.hohmann import animate_hohmann_transfer, hohmann_plot
from sim.maneuvers.inclination_change import animate_inclination_change_dv, animate_inclination_change_orb_f, compute_inclination_change_dv
from sim.visualization.animate_plan import generate_trajectory_segments, animate_burn_plan
from sim.maneuvers.burn_plan import calculate_burn_plan

# Select orbit
orbit = orb0

# show_propagation(orbit)
# animate_orbit(orbit)
# animate_hohmann_transfer(orbit, Earth.R + 18000 * u.km)
# hohmann_plot(orbit, Earth.R + 18000 * u.km)
# animate_inclination_change_dv(orb0, compute_inclination_change_dv(orb0, orb2))
# animate_inclination_change_orb_f(orb0, orb2)

plan = calculate_burn_plan(orb0, orb3)
coords, burn = generate_trajectory_segments(plan)
animate_burn_plan(coords, burn)

# show_flight_plan_propagation(coords)