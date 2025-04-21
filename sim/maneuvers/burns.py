import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sim.common_imports import *

g0 = 9.80665

def compute_delta_v(isp, m0, mf):
    dv = isp * g0 * np.log(m0 / mf)
    return dv

def simulate_burn(thrust, isp, duration, m0):
    mass_flow_rate = thrust / (isp * g0)
    mass_burned = mass_flow_rate * duration
    mf = m0 - mass_burned
    dv = compute_delta_v(isp, m0, mf)
    return dv, mf