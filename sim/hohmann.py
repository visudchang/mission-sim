import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *
from sim.orbits import orb0

dv = [5, 0, 0] << (u.m / u.s)
imp = Maneuver.impulse(dv)

def hohmann_plot(orb_i):
    hoh = Maneuver.hohmann(orb_i, 36000 << u.km)
    print(hoh.get_total_cost())
    print(hoh.get_total_time())

    fig, ax = plt.subplots()
    op = StaticOrbitPlotter(ax)
    orb_a, orb_f = orb_i.apply_maneuver(hoh, intermediate = True)
    op.plot(orb_i, label = "Initial orbit")
    op.plot(orb_a, label = "Transfer orbit")
    op.plot(orb_f, label = "Final orbit")

    plt.show()

hohmann_plot(orb0)