import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sim.common_imports import *

g0 = 9.80665

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

plot_burn(5000, 300, 2000, 500, 100, 0.0)

