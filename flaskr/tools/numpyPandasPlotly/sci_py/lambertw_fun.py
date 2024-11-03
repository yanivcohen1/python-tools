from scipy.special import lambertw
import numpy as np

result = lambertw(4)
print(result)
print("~1.2 ==",np.real(result))
