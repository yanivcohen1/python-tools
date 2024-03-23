# solve PDE Heat Equation: ∂u/∂t ​= κ*∂^2*u/∂x^2 # pylint: disable=E2515
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the PDE as a system of ODEs using the method of lines
def pde_system(t, y, N):
    dydt = np.zeros_like(y)
    dydt[1:-1] = (y[:-2] - 2*y[1:-1] + y[2:]) / dx**2  # Discretized Laplacian
    return dydt

# Set up initial conditions and parameters
N = 100  # Number of spatial points
x = np.linspace(0, 1, N)
dx = x[1] - x[0]
y0 = np.sin(np.pi * x)  # Initial condition

# Solve the PDE
solution = solve_ivp(lambda t, y: pde_system(t, y, N), [0, 1], y0, method='RK45')

# Plot the results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
X, T = np.meshgrid(x, solution.t)
ax.plot_surface(X, T, solution.y.T, cmap='viridis')

# Set labels and show the plot
ax.set_xlabel('Spatial coordinate')
ax.set_ylabel('Time')
ax.set_zlabel('Temperature')
plt.show()
