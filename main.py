from astropy import units as u
from poliastro.bodies import Earth, Sun
from poliastro.twobody import Orbit

orbit = Orbit.circular(Earth, alt = 500 * u.km)

print(f"Semi-major axis: {orbit.a}")
print(f"Orbital period: {orbit.period.to(u.minute)}")
print(f"Velocity vector: {orbit.v}")