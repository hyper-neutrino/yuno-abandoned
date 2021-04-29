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
    "⁹": Constant(sympy.Integer(256)),
    "¬": vectorize(attrdict(
        arity = 1,
        call = lambda x: int(not x)
    )),
    "½": vectorize(attrdict(
        arity = 1,
        call = sqrt
    )),
    "!": vectorize(attrdict(
        arity = 1,
        call = factorial
    )),
    "A": vectorize(attrdict(
        arity = 1,
        call = absolute
    )),
    "B": vectorize(attrdict(
        arity = 1,
        call = lambda x: tobase(x, 2)
    )),
    "×": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x * y
    )),
    "÷": vectorize(attrdict(
        arity = 2,
        call = divide
    )),
    "+": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x + y
    )),
    ",": attrdict(
        arity = 2,
        call = lambda x, y: [x, y]
    ),
    "<": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x < y
    )),
    "=": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x == y
    )),
    ">": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x > y
    )),
    "E": attrdict(
        arity = 1,
        call = all_eq
    ),
    "H": vectorize(attrdict(
        arity = 1,
        call = lambda x: [x[:len(x) // 2], x[len(x) // 2:]] if stringQ(x) else x / 2
    ), left = lambda x: not stringQ(x)),
    "_": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x - y
    )),
    "a": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x and y
    )),
    "o": vectorize(attrdict(
        arity = 2,
        call = lambda x, y: x or y
    ))
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
    "ø": lambda v, x = 0, y = 0: (),
    "µ": lambda v, x = 0, y = 0: (v,),
    "ɗ": lambda v, x = 0, y = 0: (v, y),
    "ɓ": lambda v, x = 0, y = 0: (y, v),
    "ʠ": lambda v, x = 0, y = 0: (x, v),
    "ƥ": lambda v, x = 0, y = 0: (v, x)
}
