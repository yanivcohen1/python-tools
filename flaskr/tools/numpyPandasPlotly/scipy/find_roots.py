import numpy as np
from scipy import optimize
# compute the root of f(x)=cos(x)−x
# where x is near −2
f = lambda x: np.cos(x) - x
r = optimize.fsolve(f, -2)# look for root in area of x=-2
print("r =", r) # r = [0.73908513]

# Verify the solution is a root
result = f(r)
print("result=", result) # result= [0.]
