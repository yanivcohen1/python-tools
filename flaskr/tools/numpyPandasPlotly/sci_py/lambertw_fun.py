from scipy.special import lambertw
import numpy as np

result = lambertw(4)
print(result)

# x = lambertw(x*e^x)
# x^x=4
# x*ln(x) = ln(4) , y = ln(x) => x=e^y
# y*e^y = ln(4) => W(y) = W(ln(4))
# y = ln(x) = W(ln(4))
# x = e^W(ln(4)) => x = 2
print("x^x = 4")
print("x = e^W(ln(4)) => x =",np.real(np.exp(lambertw(np.log(4)))))

# 0.5^x = x
# 0.5 = x ^ 1/x
# ln(0.5) = 1/x * ln(x), y = ln(x) => 1/x = 1/e^y = e^-y
# -y*e^-y = -ln(0.5) => W(-y) = W(-ln(0.5))
# W(-ln(x)) = W(-ln(0.5))
# -ln(x) = W(-ln(0.5))
# x = e^-W(-ln(0.5)) =~ 0.641
print("0.5^x = x")
print("x = e^-W(ln(0.5)) => x =",np.real(np.exp(-lambertw(-np.log(0.5)))))
