import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *

orb0 = Orbit.from_classical(Earth,
                             Earth.R + 500 * u.km,
                             0.0 * u.one,
                             53 * u.deg,
                             0 * u.deg,
                             0 * u.deg,
                             0 * u.deg,
                             epoch = Time("2025-01-01 00:00:00", scale = "utc"))