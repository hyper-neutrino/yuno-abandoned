from utils import *

def all_eq(item):
    if isinstance(item, list):
        return item == [] or int(all(x == item[0] for x in item[1:]))
    elif isinstance(item, sequence):
        raise SystemExit("ALL_EQ for sequences is not implemented.")
    else:
        raise SystemExit("ALL_EQ for non-iterables is not implemented.")

def divide(x, y):
    return x / y # TODO

def sqrt(x):
    if isinstance(x, str):
        raise SystemExit("sqrt string is TODO")
    return sympy.sqrt(x)

def factorial(x):
    if isinstance(x, str):
        raise SystemExit("factorial string is TODO")
    return sympy.gamma(x + 1)

def absolute(x):
    if isinstance(x, str):
        raise SystemExit("absolute value string is TODO")
    return abs(x)

def tobase(x, b):
    pass
