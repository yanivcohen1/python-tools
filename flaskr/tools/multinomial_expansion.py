from itertools import product
from math import factorial
from sympy import symbols, expand

def multinomial_coefficient(n, ks):
    """Compute multinomial coefficient n! / (k1! * k2! * ... * km!)."""
    result = factorial(n)
    for k in ks:
        result //= factorial(k)
    return result

def multinomial_expansion(vars_list, n, values=None):
    """
    Compute and display the multinomial expansion of (x1 + ... + xm)^n.
    If values is provided as a dict, it also evaluates the numeric result.

    Example:
      multinomial_expansion(['x','y','z'], 3, {'x':1, 'y':2, 'z':3})
    """
    m = len(vars_list)
    combos = [c for c in product(range(n + 1), repeat=m) if sum(c) == n]

    print(f"\n🔹 Multinomial Expansion of ({' + '.join(vars_list)})^{n}")
    print("-" * 70)

    total_value = 0  # for numeric evaluation

    for ks in combos:
        coeff = multinomial_coefficient(n, ks)
        # Build symbolic term
        term_parts = []
        term_value = coeff
        for i, var in enumerate(vars_list):
            power = ks[i]
            if power > 0:
                term_parts.append(f"{var}^{power}" if power > 1 else var)
                # numeric substitution if available
                if values and var in values:
                    term_value *= values[var] ** power
        # term = ''.join(term_parts) or "1"
        # print(f"{coeff:>4} * {term}")
        if values:
            total_value += term_value

    # Symbolic check
    sym_vars = symbols(' '.join(vars_list))
    expr = sum(sym_vars)**n
    print("\n✅ Symbolic expansion:")
    print(expand(expr))

    if values:
        print("\n🔸 Substituting values:")
        print(values)
        print(f"➡️  Numeric result: {total_value}")

# https://he.wikipedia.org/wiki/%D7%9E%D7%A9%D7%A4%D7%98_%D7%94%D7%9E%D7%95%D7%9C%D7%98%D7%99%D7%A0%D7%95%D7%9D
# Try changing n, variables, or substitution values
multinomial_expansion(['x', 'y', 'z'], 4, {'x': 1, 'y': 2, 'z': 3})
