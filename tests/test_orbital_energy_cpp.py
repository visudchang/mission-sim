import ctypes
from ctypes import c_double

lib = ctypes.CDLL("./liborbital_energy.so")

lib.compute_orbital_energy.argtypes = [c_double, c_double]
lib.compute_orbital_energy.restype = c_double

# r = 7000e3
# v = 7.8e3

def compute_orbital_energy(r, v):
    return lib.compute_orbital_energy(r, v)

# print(compute_orbital_energy(7000e3, 7.8e3))