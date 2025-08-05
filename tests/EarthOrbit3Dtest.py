import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sim.common_imports import *

def EarthOrbit3D():
    orbit = Orbit.circular(Earth, alt=500 * u.km)

    print(orbit)
    print(f"Semi-major axis: {orbit.a}")
    print(f"Orbital period: {orbit.period.to(u.minute)}")
    print(f"Velocity vector: {orbit.v}")

    fig, ax = plt.subplots(figsize=(6, 6))
    plotter = StaticOrbitPlotter(ax)
    plotter.plot(orbit, label="LEO Orbit")
    plt.show()

    plotter = OrbitPlotter3D()
    plotter.plot(orbit, label="LEO Orbit")
    plot(plotter._figure)
