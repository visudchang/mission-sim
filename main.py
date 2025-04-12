from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.plotting.static import StaticOrbitPlotter
import matplotlib.pyplot as plt
from poliastro.plotting import OrbitPlotter3D
from plotly.offline import plot
from poliastro.examples import iss

def EarthOrbit3D():
    # Create the orbit
    orbit = Orbit.circular(Earth, alt=500 * u.km)

    # Print orbital elements
    print(orbit)
    print(f"Semi-major axis: {orbit.a}")
    print(f"Orbital period: {orbit.period.to(u.minute)}")
    print(f"Velocity vector: {orbit.v}")

    # Plot using StaticOrbitPlotter
    fig, ax = plt.subplots(figsize=(6, 6))
    plotter = StaticOrbitPlotter(ax)
    plotter.plot(orbit, label="LEO Orbit")
    # plt.show()

    # Plot in 3D using Plotly
    plotter = OrbitPlotter3D()
    plotter.plot(orbit, label="LEO Orbit")
    plot(plotter._figure)

print(iss)
fig, ax = plt.subplots(figsize=(6, 6))
plotter = StaticOrbitPlotter(ax)
plotter.plot(iss, label="LEO Orbit")
plt.show()