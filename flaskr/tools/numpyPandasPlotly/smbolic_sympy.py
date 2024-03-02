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
# energy_expression = sp.sqrt((2*m*hbar**2*E) / (beta*(1 - sp.exp(-2*k*L))))

# Set parameter values
m_value = 1
hbar_value = 1
beta_value = 2
L_value = 3

# Import sympy library
import sympy as sp

# Define symbols and constants
# m, beta, hbar, L, E, k, alpha = sp.symbols('m beta hbar L E k alpha')
alpha = 2*m*beta/hbar**2 # Define alpha in terms of other symbols

# Define the equation for e^(-kL) in terms of k and alpha
eq = sp.Eq(sp.exp(-k*L), sp.Piecewise((2*k/alpha - 1, E < 0), (-2*k/alpha - 1, E > 0)))

# Solve for k using sympy's solve function
k_sol = sp.solve(eq, k)

# Print the solutions for k
print("The solutions for k are:")
for sol in k_sol:
    print(sol)

# Function to calculate energy numerically
def energy(k_value, m_value, hbar_value, beta_value, L_value, side):
    # Substitute symbolic values with numerical constants
    return k_sol[side].subs({m: m_value, hbar: hbar_value, beta: beta_value, L: L_value, k:k_value}).evalf()

# Range of wavevector values for plotting
k_vals = np.linspace(-10, 10, 100)

# Calculate energy levels numerically
energy_levels = []
for k in k_vals:
    energy_level_rhs = energy(k, m_value, hbar_value, beta_value, L_value, 0)
    energy_levels.append(energy_level_rhs)
    energy_level_lhs = energy(k, m_value, hbar_value, beta_value, L_value, 1)
    energy_levels.append(energy_level_lhs)

energy_levels_real_rhs = []
energy_levels_imag_rhs = []
energy_levels_real_lhs = []
energy_levels_imag_lhs = []
for energy_level in energy_levels:
    val = energy_level.args[0][0]
    if str(energy_level.args[0][1]).strip() == "E > 0":
        # Configure the plot for right hand side
        energy_levels_real_rhs.append(val.args[0])
        energy_levels_imag_rhs.append(val.args[1])
    else:
        # Configure the plot for left hand side
        energy_levels_real_lhs.append(val)
        # energy_levels_imag_lhs.append(lhs.args[1])

# Plot the real part
plt.plot(k_vals, energy_levels_real_rhs, label='Real part right hand side')
# plt.plot(k_vals, np.imag(energy_levels_imag_rhs), "--" , label='imag part right hand side')
plt.plot(k_vals, energy_levels_real_lhs, label='Real part left hand side')
# plt.plot(k_vals, np.imag(energy_levels_imag_lhs), "--" , label='imag part left hand side')
# plt.plot(k_vals[1:], energy_levels_imag[1:], label='imag part')

# plt.plot(k_vals, energy_levels, label="Energy Levels")
plt.xlabel("Wavevector (k)")
plt.ylabel("Energy (E)")
plt.title("Energy Levels of Pair of Delta Wells")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
