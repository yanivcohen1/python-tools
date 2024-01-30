import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# https://matplotlib.org/stable/gallery/
# https://www.youtube.com/watch?v=xcONCZR6bMo&t=263s
# https://github.com/derekbanas/Python4Finance/blob/main/Numpy_Pandas.ipynb
# -------- panda for data menipulation -------------------
csv = {
  'cars': ["BMW", "Volvo", "Ford"],
  'time': [1, 2, 3],
  'passings': [3, 7, 2]
}

table = pd.DataFrame(csv, columns=['time', 'passings'])# option to fillter
# table = pd.read_csv('data.csv')

# Panda print 2 first rows
# use a list of indexes:
print(table.loc[[0, 1]])
#     cars  passings
# 0    BMW         3
# 1  Volvo         7

# panda plot
table.plot()
plt.xlabel('Time')
plt.ylabel('Wave function')
plt.title('plot for panda data')
plt.show()

# ------ nupmy for math ----------------------

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
