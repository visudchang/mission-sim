import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sim.common_imports import *
from sim.visualization.animated_orbit import animate_orbit
from sim.maneuvers.hohmann import animate_hohmann_transfer, hohmann_plot
from sim.maneuvers.inclination_change import animate_inclination_change_dv, animate_inclination_change_orb_f, compute_inclination_change_dv
from sim.orbits import orb0, orb2

@dataclass
class ManeuverStep:
    name: str
    orbit: Orbit
    duration: u.Quantity
    burn: bool = False

def calculate_burn_plan(orb_i, orb_target):
    plan = []

    hoh = Maneuver.hohmann(orb_i, orb_target.a)
    hoh_orbits = orb_i.apply_maneuver(hoh, intermediate = True)
    orb_transfer, orb_f = hoh_orbits

    plan.append(ManeuverStep("Initial Orbit", orb_i, orb_i.period, burn = False))
    plan.append(ManeuverStep("Hohmann Transfer", orb_transfer, orb_transfer.period / 2, burn = True))

    if abs((orb_f.inc - orb_target.inc).to(u.deg).value) > 0.01:
        dv = compute_inclination_change_dv(orb_f, orb_target)
        orb_f = orb_f.apply_maneuver(Maneuver.impulse(dv))
        plan.append(ManeuverStep("Inclination Change", orb_f, orb_f.period, burn = True)) 

    return plan   