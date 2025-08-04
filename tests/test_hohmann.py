import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.maneuvers.hohmann import animate_hohmann_transfer, hohmann_plot, hohmann_transfer_dv

def test_hohmann_to_geostationary():
    leo = Orbit.circular(Earth, alt = 300 * u.km)
    geo = Orbit.circular(Earth, alt = 35786 * u.km)
    dv = hohmann_transfer_dv(leo, geo.a)

    assert dv.value > 3.7
    assert dv.value < 4.1

