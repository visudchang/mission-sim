import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.maneuvers.inclination_change import compute_inclination_change_dv

def test_inclination_change():
    orb_i = Orbit.circular(Earth, alt = 300 * u.km, inc = 0 * u.deg)
    orb_f = Orbit.circular(Earth, alt = 300 * u.km, inc = 40 * u.deg)
    dv = np.linalg.norm(compute_inclination_change_dv(orb_i, orb_f))

    assert dv.value > 5.1
    assert dv.value < 5.4
