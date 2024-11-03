from scipy.special import lambertw
import numpy as np

result = lambertw(4)
print(result)
print("~1.2 ==",np.real(result))

# x = lambertw(x*e^x)
# x^x=4
# x = e^W(ln(4)) == 2
# x = ln(4)/W(ln(4))

# 0.5^x = x
# x = W(ln(2))/ln(2) =~ 1.2
