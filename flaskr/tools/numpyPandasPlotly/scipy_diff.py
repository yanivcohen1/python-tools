# solve eq -> y"(x) +9y(x) = 0, let y(0) = 1 and y'(0) = 0
# the solution is -> y(x) = cos(3*x)

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the differential equation as a system of first-order equations
def dydx(y, x):
    y1 = y[0] # y
    y2 = y[1] # y'
    dy1dx = y2 # y' = dy/dx
    dy2dx = -9 * y1 # y'' = -9y
    return [dy1dx, dy2dx]

# Define the initial conditions
y0 = [1, 0] # y(0) = 1, y'(0) = 0

# Define the range of x values
x = np.linspace(-10, 10, 100)

# Solve the differential equation numerically
y = odeint(dydx, y0, x)

# Plot the solution
plt.plot(x, y[:, 0], label='y')
plt.plot(x, y[:, 1], label="y'")
plt.xlabel('x')
plt.ylabel('y, y\'')
plt.title('Solution of y\'\' + 9y = 0')
plt.legend()
plt.grid(True)
plt.show()
