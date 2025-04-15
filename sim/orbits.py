import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *

orb0 = Orbit.from_classical(cfg["attractor"],
                            cfg["a"],
                            cfg["ecc"],
                            cfg["inc"],
                            cfg["raan"],
                            cfg["argp"],
                            cfg["nu"],
                            epoch = cfg["epoch"])

orb1 = Orbit.from_classical(cfg["attractor"],
                            Earth.R + 36000 * u.km,
                            cfg["ecc"],
                            cfg["inc"],
                            cfg["raan"],
                            cfg["argp"],
                            cfg["nu"],
                            epoch = cfg["epoch"])

orb2 = Orbit.from_classical(cfg["attractor"],
                            cfg["a"],
                            cfg["ecc"],
                            53.0 * u.deg,
                            cfg["raan"],
                            cfg["argp"],
                            cfg["nu"],
                            epoch = cfg["epoch"])

orb3 = Orbit.from_classical(cfg["attractor"],
                            cfg["a"] + 18000 * u.km,
                            cfg["ecc"],
                            53.0 * u.deg,
                            cfg["raan"],
                            cfg["argp"],
                            cfg["nu"],
                            epoch = cfg["epoch"])