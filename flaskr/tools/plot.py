import numpy as np
import matplotlib.pyplot as plt

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
plt.xlabel('Time')
plt.ylabel('Wave function')
plt.title('Real part of the wave function at x=0')
# plt.legend()
# plt.show()

# Plot the imaginary part
plt.plot(t, psi_imag, label='Imaginary part')
plt.xlabel('Time')
plt.ylabel('Wave function')
plt.title('The wave function at x=0')
plt.legend()
plt.show()
