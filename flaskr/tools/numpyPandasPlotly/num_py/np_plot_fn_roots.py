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
# Find indices where the sign changes
crossing_indices = np.where(np.diff(np.sign(y)) != 0)[0]
# print("Indices where sign changes:", crossing_indices)

# Compute the zero crossing points via linear interpolation
x_crossings = []
for idx in crossing_indices:
    # Get points on either side of the crossing
    x1, x2 = x[idx], x[idx+1]
    y1, y2 = y[idx], y[idx+1]

    # Avoid division by zero (if y2 == y1, it might need special handling)
    if y2 - y1 == 0:
        continue

    # Linear interpolation formula
    x_zero = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
    x_crossings.append(x_zero)

print("Zero crossings (x-coordinates):", x_crossings)

# Plotting the equation and the solutions
if len(x_crossings) > 0:
    plt.figure(figsize=(10, 6))
    # Show the solutionss on the plot
    for sol in x_crossings:
        plt.annotate(f'{sol:.2f}', xy=(sol, 0), xytext=(0, 10),
            textcoords='offset points', ha='center', color='red')
    # Plot the function
    plt.plot(x, y, label='3sin(2x) + 4cos(x) - 5')
    plt.axhline(0, color='r', linestyle='--', label='y=0 (Target)') # Mark y=0
    # Mark the solutionss as green o points
    plt.plot(x_crossings, np.zeros_like(x_crossings), 'go', markersize=8, label='Solutions (roots)')
    plt.xlabel('x')
    plt.ylabel('3sin(2x) + 4cos(x) - 5')
    plt.title('Plot of the equation and the solutions')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("Plotting not possible as no solutions was found.")
