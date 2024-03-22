# f(x, y) = x² + y² - 10.0 = 0
# g(x, y) = x + y + k = 0 ; for 1<= k <=3
# You should get x = 0.1583124, y = -3.1583124
# if you start with x = y = 1 as an initial guess.
from scipy.optimize import fsolve

def h(z, k):
    x = z[0]
    y = z[1]
    f = x**2 + y**2 - 10.0
    g = x + y+ 1*k
    return [f,g]

z0 = [1,1]
for k in [1,2,3]:
    print(f"for k={k}: ", fsolve(h, z0, args=(k)))
# the output is [x_root, y_root]:
# for k=1:  [-2.67944947  1.67944947]
# for k=2:  [ 1. -3.]
# for k=3:  [ 0.1583124 -3.1583124]
