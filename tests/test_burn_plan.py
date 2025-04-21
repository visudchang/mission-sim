import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.maneuvers.burn_plan import calculate_burn_plan

def test_burn_plan():
    orb_i = Orbit.circular(Earth, alt = 300 * u.km, inc = 0 * u.deg)
    orb_f = Orbit.circular(Earth, alt = 35786 * u.km, inc = 50 * u.deg)
    plan = calculate_burn_plan(orb_i, orb_f)

    assert len(plan) == 3
