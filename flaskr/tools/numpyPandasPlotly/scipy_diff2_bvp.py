import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt


# Define the differential equation as a system of first-order ODEs
def ode_system(x, y, p):
    k = p[0]
    return np.vstack((y[1], -(k**2) * y[0]))


# Boundary conditions
def bc(ya, yb, p):
    return np.array([ya[0], yb[0], ya[1] - p[0]])


# Initial mesh
x = np.linspace(0, 1, 5)

# Initial guess for the solution and parameter k
y_guess = np.zeros((2, x.size))
y_guess[0, 1] = 1
y_guess[0, 3] = -1

k_guess = []
errors = []

for k in range(1, 10):
    k_gues = np.array([k])

    # Solve the BVP
    sol = solve_bvp(ode_system, bc, x, y_guess, p=k_gues)

    # Verify if the solution was successful
    if sol.success:
        errors.append(np.abs(k - sol.p[0]))
        k_guess.append(k)
    else:
        print(f"when k={k} The solver did not converge to a solution.")

# plot k Predicted vs Error in Guess
plt.plot(k_guess, errors, marker=".")
plt.xlabel("Predicted k")
plt.ylabel("Error in guess")
plt.title("k Predicted vs Error in Guess")
plt.grid()
plt.show()

# plot the solution at min error for k
x_plot = np.linspace(0, 1, 100)
k = k_guess[np.argmin(errors)]
sol = solve_bvp(ode_system, bc, x, y_guess, p=[k])
y_plot = sol.sol(x_plot)[0]
plt.plot(x_plot, y_plot, label="y = sin(k * x)")
plt.title(f"Solution at k={k} where minimum Error in Guess")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
