import numpy as np
import matplotlib.pyplot as plt

# Define the function that we want to find the root for:
# 3sin(2x) + 4cos(x) = 5  =&gt;  3sin(2x) + 4cos(x) - 5 = 0
def equation_to_solve(x):
    return 3 * np.sin(2*x) + 4 * np.cos(x) - 5

x = np.linspace(-np.pi, np.pi, 500) # Range for plotting (0 to 2pi for trigonometric functions)
y = equation_to_solve(x)
# Find indices where the sign of y changes.
# This means consecutive points where y values have opposite signs.
sign_changes = np.where(np.diff(np.sign(y)))[0]

# List to hold the crossing points (x values where y=0)
crossings = []

# For each sign change, perform a linear interpolation to find the crossing x-coordinate.
for i in sign_changes:
    x0, y0 = x[i], y[i]
    x1, y1 = x[i + 1], y[i+1]
    # Linear interpolation formula to find x where y = 0:
    # x_cross = x0 - y0 * (x1 - x0) / (y1 - y0)
    x_cross = x0 - y0 * (x1 - x0) / (y1 - y0)
    crossings.append(x_cross)

# Plotting the equation and the solutions
if len(crossings) > 0:
    plt.figure(figsize=(10, 6))
    # Show the solutionss on the plot
    for sol in crossings:
        plt.annotate(f'{sol:.2f}', xy=(sol, 0), xytext=(0, 10),
            textcoords='offset points', ha='center', color='red')
    # Plot the function
    plt.plot(x, y, label='3sin(2x) + 4cos(x) - 5')
    plt.axhline(0, color='r', linestyle='--', label='y=0 (Target)') # Mark y=0
    # Mark the solutionss as green o points
    plt.plot(crossings, np.zeros_like(crossings), 'go', markersize=8, label='Solutions (roots)')
    plt.xlabel('x')
    plt.ylabel('3sin(2x) + 4cos(x) - 5')
    plt.title('Plot of the equation and the solutions')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("Plotting not possible as no solutions was found.")
