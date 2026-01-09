# Numerically solve
#   H psi = E psi
# for a system of particle in a 1D box.

import numpy as np

# physical parameters in natural units
hbar = 1.0
m = 1.0
L = 1.0

# numerical parameters
N = 100 # num of grid points
dx = L / (N + 1)

# compose T: kinetic energy matrix
diag = -2.0 * np.ones(N)
offdiag = 1.0 * np.ones(N - 1)

laplacian = (np.diag(diag) +
             np.diag(offdiag, k=1) +
             np.diag(offdiag, k=-1)) / dx**2

T = -(hbar**2) / (2 * m) * laplacian

# compose V: potential energy matrix (zero inside the box)
V = np.zeros((N, N))

# compose H: hamiltonian of the physical system
H = T + V

# diagonalize H
energies, states = np.linalg.eigh(H)

# also calculate analytic energies for comparison
n = np.arange(1, 6)
E_analytic = (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)

print("Lowest 5 numberical energies:")
print(energies[:5])

print("\nLowest 5 analytic energies:")
print(E_analytic)