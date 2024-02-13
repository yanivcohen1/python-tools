import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# https://matplotlib.org/stable/gallery/
# https://www.youtube.com/watch?v=xcONCZR6bMo&t=263s
# https://github.com/derekbanas/Python4Finance/blob/main/Numpy_Pandas.ipynb

# -------- panda for table data menipulation -------------------
csv = {
  "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
  "Profit": [200, 300, 400, 500, 600, 700],
  'time': [1, 2, 3],
}

table = pd.DataFrame(csv, columns=['Month', 'Sales', "Profit"])# option to fillter
# table = pd.read_csv('data.csv')

# Panda print 2 first rows
# use a list of indexes:
print(table.loc[[0, 1]])
#     cars  passings
# 0    BMW         3
# 1  Volvo         7

# create a figure and an Axes
fig, ax = plt.subplots()

# plot a line plot of the Sales column with points
table.plot.line(x="Month", y="Sales", ax=ax, marker="o", markersize=10)

# plot a line plot of the Profit column on a secondary y-axis
table.plot.line(x="Month", y="Profit", ax=ax, secondary_y=True, marker="o", markersize=10)

# show the figure
plt.show()

# ------ nupmy for math 2d and 3d ----------------------

# Define the parameters
a = 1 # length scale
hbar = 1 # reduced Planck constant
m = 1 # mass

# Define the time range
t = np.linspace(0, 10, 100)

# Define the wave function at x=0
psi = 1/np.sqrt(np.pi*a**2)*np.exp(-1j*hbar/a**2*t)

# Extract the real and imaginary parts
psi_real = np.real(psi)
psi_imag = np.imag(psi)

# Plot the real part
plt.plot(t, psi_real, label='Real part')
# plt.xlabel('Time')
# plt.ylabel('Wave function')
# plt.title('Real part of the wave function at x=0')
# plt.legend()
# plt.show()

# Plot the imaginary part
plt.plot(t, psi_imag, label='Imaginary part')
plt.xlabel('Time')
plt.ylabel('Wave function')
plt.title('plot for numpy data')
plt.legend()
plt.show()
