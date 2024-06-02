import matplotlib.pyplot as plt
import numpy as np

x_d = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
y_d = np.array([0, 0.8, 0.9, 0.1, -0.6, -0.8, -1, -0.9, -0.4])

plt.figure(figsize = (12, 6))
for i in range(1, 7):

    # get the polynomial coefficients
    y_est = np.polyfit(x_d, y_d, i)
    plt.subplot(2,3,i)
    plt.plot(x_d, y_d, 'o')
    # evaluate the values for a polynomial
    plt.plot(x_d, np.polyval(y_est, x_d))
    plt.title(f'Polynomial order {i}')
    # print poly
    print(f"poly {i}: ", end="")
    for j in range(i + 1):
        if j-i == 0:
            print(f"{y_est[i-j]:.2f}", end=" ")
        else:
            print(f"{y_est[i-j]:.2f} X^{i-j} +", end=" ")
    print("")

plt.tight_layout()
plt.show()
