# solve eq -> y"(x) +9y(x) = 0, let y(0) = 1 and y'(0) = 0
# the solution is -> y(x) = cos(3*x)

from sympy import Function, dsolve, symbols, Eq
import matplotlib.pyplot as plt
import numpy as np

y = Function('y')
x = symbols('x')

# Define the ODE as an equation
ode = Eq(y(x).diff(x, x) + 9*y(x), 0)

# Add starting terms to the ODE equation
# For example, let y(0) = 1 and y'(0) = 0
# This means that the initial value of y is 1 and the initial value of y' is 0
# To add these starting terms, we use the ics argument of dsolve
ics = {y(0): 1, y(x).diff(x).subs(x, 0): 0}

# Solve the ODE using dsolve with the ics argument
sol = dsolve(ode, y(x), ics=ics)

# Print the solution
print(sol)


# Function to calculate energy numerically
def fill_vals(x_value):
    # Substitute symbolic values with numerical constants
    return (
        sol
        .subs({x: x_value})
        .evalf()
    )

x_vals = np.linspace(-10, 10, 100)

# Calculate energy levels numerically
energy_levels = []
for x_val in x_vals:
    energy_level_rhs = fill_vals(x_val)
    energy_levels.append(energy_level_rhs.args[1])

plt.plot(x_vals, energy_levels, label="cos(3*x)")
# plt.plot(k_vals, np.imag(energy_levels_imag_rhs), "--" , label='imag part right hand side')

# plt.plot(k_vals, energy_levels, label="Energy Levels")
plt.xlabel("position(x)")
plt.ylabel("Y(x)")
plt.title("solve y''(x) +9y(x) = 0, let y(0) = 1 and y'(0) = 0")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
