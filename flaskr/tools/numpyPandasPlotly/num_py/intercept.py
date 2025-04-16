import numpy as np
import matplotlib.pyplot as plt

# Define grid
x = np.linspace(-1.5, 1.5, 400)
y = np.linspace(-1.5, 1.5, 400)
X, Y = np.meshgrid(x, y)

# Define region: inside unit circle and above y = x
region = (X**2 + Y**2 < 1) & (Y > X)

# Convert boolean to integer (1 for True, 0 for False)
region_int = region.astype(int)

# Plot only the region where condition is True (value = 1)
plt.figure(figsize=(6,6))
plt.contourf(X, Y, region_int, levels=[0.5, 1.5], colors=["blue"])
plt.xlabel("x")
plt.ylabel("y")
plt.title("Region: $x^2 + y^2 < 1$ and $y > x$")
plt.axis("equal")
plt.grid(True)
plt.show()
