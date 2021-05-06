import interpreter

from utils import *

from extras import *

register = 0

functions = {
    "®": attrdict(arity = 0, call = lambda: register),
    "³": Constant("\n"),
    "⁴": Constant(" "),
    "⁵": Constant(sympy.Integer(100)),
    "⁶": Constant(sympy.Integer(16)),
    "⁷": Constant(sympy.Integer(10)),
    "⁸": Constant([]),
    "⁹": Constant(sympy.Integer(256))
}

operators = {
    "@": lambda stack: (lambda func: attrdict(
        arity = 2,
        call = lambda x, y: func.call(y, x)
    ))(stack.pop()),
    "Ç": lambda stack: attrdict(
        arity = 1,
        call = lambda x: interpreter.quick_invoke(interpreter.ilist[-1] - 1, x)
    ),
}

directives = {
    "µ": lambda v, x = 0, y = 0: (v,),
    "ɗ": lambda v, x = 0, y = 0: (v, y),
    "ɓ": lambda v, x = 0, y = 0: (y, v),
    "ʠ": lambda v, x = 0, y = 0: (x, v),
    "ƥ": lambda v, x = 0, y = 0: (v, x)
}
