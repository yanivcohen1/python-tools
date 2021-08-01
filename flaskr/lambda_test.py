import math

def x(a, b, c): return a + b + c

# print 6
print(x(1, 2, 3))
# print 5
print((lambda x, y: x + y)(2, 3))

def myfunc(n):
    return lambda a: a + n * 2

# int the function for n param
the_ret_lambda_fun = myfunc(2)
# print 14 init the lambda for a=10 the n stay n=2
print(the_ret_lambda_fun(10))
# print 9
print(f"the_ret_lambda_fun(5) = {the_ret_lambda_fun(5)}")

# taylor serial to sin function
def taylor_sin(angle: float):
    i: int
    sinus: float = 0
    sign: int = 1
    factorial: int = 1
    power: float = angle
    for i in range(10):
        sinus += sign * power / factorial
        sign = -sign
        factorial *= (2 * i + 2) * (2 * i + 3)
        power *= angle * angle
    return(sinus)

def taylor_e(angle: float):
    i: int
    sinus: float = 0
    sign: int = 1
    factorial: int = 1
    power: float = angle
    for i in range(10):
        sinus += 1/factorial
        sign = -sign
        factorial *= i+1
    return(sinus)

# test taylor serial to sin function
print("sin 30 degree or pi/6: " + str(taylor_sin(math.pi/3)))
print("sin 30 form math lib: " + str(math.sin(math.pi/6)))
print("calc e: " + str(taylor_e(0)))