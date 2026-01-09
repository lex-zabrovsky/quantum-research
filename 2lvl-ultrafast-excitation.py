import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- 1. Physical Parameters ---
omega_0 = 1.0          # Transition frequency (normalized)
omega_c = 1.1          # Carrier frequency (slightly detuned to see dynamics)
tau = 6.0              # Pulse duration (FWHM-like)
t_0 = 15.0             # Center of the pulse
phi = 0.0              # Carrier-Envelope Phase (CEP)
Omega_0 = 0.6          # Peak Rabi frequency

# --- 2. Definition of the Field and the TDSE ---
def field(t):
    """Ultrafast electric field with Gaussian envelope"""
    # Standard Gaussian: exp(-t^2 / 2*sigma^2)
    # sigma = tau / (2 * sqrt(2 * ln(2))) approx tau / 2.355
    sigma = tau / 2.355
    envelope = Omega_0 * np.exp(-(t - t_0)**2 / (2 * sigma**2))
    return envelope * np.cos(omega_c * t + phi)

def system_dynamics(t, y):
    """
    y[0], y[1] are real and imaginary parts of c_g
    y[2], y[3] are real and imaginary parts of c_e
    """
    cg = complex(y[0], y[1])
    ce = complex(y[2], y[3])
    
    E_t = field(t)
    
    # Schrodinger: d/dt |psi> = -i/hbar H |psi> (hbar=1)
    # dcg/dt = -i * (-0.5*w0*cg - E_t*ce)
    # dce/dt = -i * (0.5*w0*ce - E_t*cg)
    dcg = -1j * (-0.5 * omega_0 * cg - E_t * ce)
    dce = -1j * (0.5 * omega_0 * ce - E_t * cg)
    
    return [dcg.real, dcg.imag, dce.real, dce.imag]

# --- 3. Execution ---
t_span = (0, 30)
t_eval = np.linspace(0, 30, 2000) # High resolution to capture wiggles
y0 = [1.0, 0.0, 0.0, 0.0]        # Pure ground state at t=0

sol = solve_ivp(system_dynamics, t_span, y0, t_eval=t_eval, method='RK45', rtol=1e-8)

# Reconstruct complex amplitudes
cg = sol.y[0] + 1j*sol.y[1]
ce = sol.y[2] + 1j*sol.y[3]

# Calculate populations
prob_g = np.abs(cg)**2
prob_e = np.abs(ce)**2

# --- 4. Visualization ---
plt.figure(figsize=(10, 6))
plt.plot(t_eval, prob_e, label='Excited State Population $P_e(t)$', color='darkorange', lw=2)
plt.plot(t_eval, field(t_eval)/Omega_0, '--', color='gray', alpha=0.3, label='Pulse Envelope (scaled)')

plt.title(f'Ultrafast Dynamics Beyond RWA ($\omega_c={omega_c}, \Omega_0={Omega_0}$)')
plt.xlabel('Time (1/$\omega_0$)')
plt.ylabel('Population / Field Amplitude')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('phase_map.png')
print("Done! Open 'phase_map.png' to see the results.")