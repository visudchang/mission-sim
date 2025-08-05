import os
import ctypes
from ctypes import c_double

lib_path = os.path.join(os.path.dirname(__file__), "../liborbital_energy.so")
lib_path = os.path.abspath(lib_path)

lib = ctypes.CDLL(lib_path)

lib.compute_orbital_energy.argtypes = [c_double, c_double]
lib.compute_orbital_energy.restype = c_double

# r = 7000e3
# v = 7.8e3

def compute_orbital_energy(r, v):
    return lib.compute_orbital_energy(r, v)

# print(compute_orbital_energy(7000e3, 7.8e3))