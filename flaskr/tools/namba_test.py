import numpy as np
from numba import jit, objmode
import pandas as pd
import time

# Create a NumPy array (avoid dtype=object)
A = np.array([[2, 5], [4, 5], [0, 8], [6, 7], [1, 8], [0, 1], [1, 3], [1, 3], [2, 4]], dtype=np.int32)
B = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int)

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Define a function to optimize with Numba
@jit(nopython=True)
def f(A: np.ndarray, B: np.ndarray) -> float:
    total = 0.0
    for i in range(len(B)):
        total += g(A[i], B)
    return total

def bar(x):
    # This code is executed by the interpreter.
    df = pd.DataFrame(data, columns=['Numbers'])
    return np.asarray(x.tolist()) + np.asarray(df['Numbers'])

# Define another function (simplified representation of your actual function)
@jit(fastmath=True)
def g(a: np.ndarray, B: np.ndarray) -> float:
    # Some function of 'a' and 'B'
    with objmode(y='intp[:]'):  # annotate return type integer pointer
        # this region is executed by object-mode.
        y = bar(B)
    return 19.12 / (len(a) + len(B) + sum(y))

# Call the optimized function
start = time.time()
result = f(A, B)
print("Result:", result)
print(f'run toke {time.time()-start:.2f} sec')
