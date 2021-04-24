import interpreter

from utils import *

functions = {
    "³": Constant("\n"),
    "⁴": Constant(" "),
    "⁵": Constant(100),
    "⁶": Constant(16),
    "⁷": Constant(10),
    "⁸": Constant([]),
    "⁹": Constant(256),
    "_": attrdict(
        arity = 2,
        call = lambda x, y: x - y
    ),
    "+": attrdict(
        arity = 2,
        call = lambda x, y: x + y
    ),
    ",": attrdict(
        arity = 2,
        call = lambda x, y: [x, y]
    ),
    "H": attrdict(
        arity = 1,
        call = lambda x: x / 2
    )
}

operators = {
    "@": lambda stack: (lambda func: attrdict(
        arity = 2,
        call = lambda x, y: func.call(y, x)
    ))(stack.pop()),
    "Ç": lambda stack: attrdict(
        arity = 1,
        call = lambda x: interpreter.quick_invoke(interpreter.ilist[-1] - 1, x)
    )
}

directives = {
    "ø": lambda v, x = 0, y = 0: (),
    "µ": lambda v, x = 0, y = 0: (v,),
    "ɗ": lambda v, x = 0, y = 0: (v, y),
    "ɓ": lambda v, x = 0, y = 0: (y, v),
    "ʠ": lambda v, x = 0, y = 0: (x, v),
    "ƥ": lambda v, x = 0, y = 0: (v, x)
}
