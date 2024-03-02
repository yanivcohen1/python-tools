import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Define constants symbolically
m = sp.Symbol('m', positive=True)
hbar = sp.Symbol('hbar')
beta = sp.Symbol('beta', positive=True)
L = sp.Symbol('L', positive=True)

# Define energy as a symbol
E = sp.Symbol('E')
k = sp.Symbol('k')
# Replace with your symbolic solution for energy (assuming k is the wavevector)
energy_expression = sp.sqrt((2*m*hbar**2*E) / (beta*(1 - sp.exp(-2*k*L))))

# Function to calculate energy numerically
def energy(k_value, m_value, hbar_value, beta_value, L_value):
    # Substitute symbolic values with numerical constants
    E_value = E
    return energy_expression.subs({m: m_value, hbar: hbar_value, beta: beta_value, L: L_value, E:1, k:k_value}).evalf()

# Set parameter values
m_value = 1
hbar_value = 1
beta_value = 2
L_value = 3

# Range of wavevector values for plotting
k_vals = np.linspace(0, 10, 100)

# Calculate energy levels numerically
energy_levels = []
for k_val in k_vals:
    energy_level = energy(k_val, m_value, hbar_value, beta_value, L_value)
    energy_levels.append(energy_level)

# Configure the plot
energy_levels_real = np.real(energy_levels)
energy_levels_imag = np.imag(energy_levels)

# Plot the real part
plt.plot(k_vals[1:], energy_levels_real[1:], label='Real part')
# plt.plot(k_vals[1:], energy_levels_imag[1:], label='imag part')

# plt.plot(k_vals, energy_levels, label="Energy Levels")
plt.xlabel("Wavevector (k)")
plt.ylabel("Energy (E)")
plt.title("Energy Levels of Pair of Delta Wells")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
