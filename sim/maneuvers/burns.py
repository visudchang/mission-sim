import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sim.common_imports import *

g0 = 9.80665

def periapsis_adjustment_dv(rp_current, rp_target, ra_fixed, mu=398600.4418):
    a_current = (rp_current + ra_fixed) / 2
    a_target = (rp_target + ra_fixed) / 2
    v_current = np.sqrt(mu * (2/ra_fixed - 1/a_current))
    v_target = np.sqrt(mu * (2/ra_fixed - 1/a_target))
    return (v_target - v_current) * u.km / u.s

def time_to_periapsis(orbit):
    # Extract orbital parameters
    ecc = orbit.ecc.value
    a = orbit.a.to(u.km).value
    nu = orbit.nu.to(u.rad).value
    mu = orbit.attractor.k.to(u.km**3 / u.s**2).value

    # Step 1: Compute eccentric anomaly E from true anomaly nu
    cos_E = (ecc + np.cos(nu)) / (1 + ecc * np.cos(nu))
    E = np.arccos(np.clip(cos_E, -1.0, 1.0))
    if nu > np.pi:
        E = 2 * np.pi - E

    # Step 2: Compute mean anomaly M
    M = E - ecc * np.sin(E)

    # Step 3: Compute mean motion n
    n = np.sqrt(mu / a**3)  # radians per second

    # Step 4: Time to periapsis
    period = 2 * np.pi / n
    time_since_periapsis = M / n
    time_until_periapsis = period - time_since_periapsis

    return time_until_periapsis * u.s


def compute_delta_v(isp, m0, mf):
    dv = isp * g0 * np.log(m0 / mf)
    return dv

def simple_burn(thrust, isp, duration, m0):
    mass_flow_rate = thrust / (isp * g0)
    mass_burned = mass_flow_rate * duration
    mf = m0 - mass_burned
    dv = compute_delta_v(isp, m0, mf)
    return dv, mf

def plot_burn(thrust, isp, duration, m0, dry_mass, v0):
    mass_flow_rate = thrust / (isp * g0)
    dt = 0.5
    times = [0.0]
    mass = [m0]
    acceleration = []
    velocity = [v0]
    while times[-1] < duration:
        current_mass = mass[-1]
        if current_mass <= dry_mass:
            print(f"Burn ended at t = {times[-1]:.1f}s — fuel exhausted.")
            break
        times.append(times[-1] + dt)
        new_mass = current_mass - mass_flow_rate * dt
        new_mass = max(new_mass, dry_mass)
        mass.append(new_mass)
        a = thrust / new_mass
        acceleration.append(a)
        v = velocity[-1] + a * dt
        velocity.append(v)

    dv = velocity[-1] - v0
    print(f"Total delta v: {dv} m/s")

    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    axs[0].plot(times, mass, color='tab:green')
    axs[0].set_ylabel('Mass (kg)')
    axs[0].set_title('Mass vs Time')
    axs[0].grid(True)

    axs[1].plot(times, velocity, color='tab:blue')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].set_title('Velocity vs Time')
    axs[1].grid(True)

    axs[2].plot(times[:-1], acceleration, color='tab:orange')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Acceleration (m/s²)')
    axs[2].set_title('Acceleration vs Time')
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

# plot_burn(5000, 300, 2000, 500, 100, 0.0)

def perform_burn(orbit, thrust, isp, duration, m0):
    dv, mf = simple_burn(thrust, isp, duration, m0)
    burn = Maneuver.impulse([0, dv, 0]  * u.m / u.s)
    new_orbit = orbit.apply_maneuver(burn)
    return new_orbit, mf
