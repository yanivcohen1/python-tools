# https://www.youtube.com/watch?v=slbZ-SLpIgg
import numpy as np
import matplotlib.pyplot as plt

num_sims = 1000000 # number of trays

A = np.random.uniform(1, 5, num_sims) # uniform prabbility between 1 to 5
B = np.random.uniform(2, 6, num_sims) # uniform prabbility between 2 to 6

duration = A + B # probbility of a and b for finish A and then finish B

plt.figure()
plt.hist(duration, density = True, edgecolor='white')
plt.axvline(9, color='r')
res = (duration > 9).sum()/num_sims * 100 # 100 for precentages
plt.title(f"your probbility of a and b after 9 is: {res:.2f}%")
plt.show()
