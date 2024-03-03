# solve eq -> y"(x) +9y(x) = 0
# the solution is -> y(x) = C1*sin(3x) + C2*cos(3x)

from sympy import Function, dsolve, symbols, Eq
y = Function('y')
x = symbols('x')

# Define the ODE as an equation
ode = Eq(y(x).diff(x, x) + 9*y(x), 0)

# Solve the ODE using dsolve
sol = dsolve(ode, y(x))

# Print the solution
print(sol)
