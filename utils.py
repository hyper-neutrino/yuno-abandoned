import codepage, commands, dictionary, sympy, sys

flags = sys.argv[1]

class attrdict(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)
        self.__dict__ = self

class Constant:
    def __init__(self, value):
        self.arity = 0
        self.value = value
    def call(self, *args, **kwargs):
        return self.value
    def __str__(self):
        return f"<Constant Function: {self.value}>"
    def __repr__(self):
        return str(self)

class sequence:
    def __init__(self, next):
        self._next = next
        self.mem = []
    @classmethod
    def by_function(self, func, start = 1, step = 1):
        def inner_next():
            value = func(start)
            start += step
            return value
        return sequence(inner_next)
    def ensure(self, count):
        while len(self.mem) < count:
            self.next()
    def __getitem__(self, index):
        self.ensure(index + 1)
        return self.mem[index]
    def next(self):
        val = self._next()
        self.mem.append(val)
        return val
    def __str__(self):
        self.ensure(10)
        return "[%s, ...]" % ", ".join(map(str, self.mem[:10]))
    def __repr__(self):
        return str(self)

class arithmetic_sequence(sequence):
    def __init__(self, initial, delta):
        sequence.__init__(self, self._next)
        self.term = initial
        self.delta = delta
    def _next(self):
        value = self.term
        self.term = commands.functions["+"].call(self.term, self.delta)
        return value

class geometric_sequence(sequence):
    def __init__(self, initial, ratio):
        sequence.__init__(self, self._next)
        self.term = initial
        self.ratio = ratio
    def _next(self):
        value = self.term
        self.term = commands.functions["×"].call(self.term, self.ratio)
        return value

class looping_sequence(sequence):
    def __init__(self, terms):
        sequence.__init__(self, self._next)
        eq = all(x == terms[0] for x in terms[1:])
        self.index = 0
        self.terms = terms
    def _next(self):
        self.index += 1
        return self.terms[(self.index - 1) % len(self.terms)]

def coerce(x):
    if isinstance(x, tuple) or isinstance(x, set):
        return list(x)
    return x

def yuno_typify(x):
    if isinstance(x, str):
        return list(x)
    if isinstance(x, complex):
        return x.real + x.imag * sympy.I
    if isinstance(x, int) or isinstance(x, float):
        return sympy.Number(x)
    try:
        a = [yuno_typify(y) for y in x]
        if a[-1] == ...:
            if len(a) >= 3:
                try:
                    diffs = [commands.functions["_"].call(y, x) for x, y in zip(a[:-2], a[1:-1])]
                    if all(x == diffs[0] for x in diffs[1:]):
                        return arithmetic_sequence(a[0], diffs[0])
                except:
                    pass
                try:
                    rates = [commands.functions["÷"].call(y, x) for x, y in zip(a[:-2], a[1:-1])]
                    if all(x == rates[0] for x in rates[1:]):
                        return geometric_sequence(a[0], rates[0])
                except:
                    pass
            return looping_sequence(a[:-1])
        return a
    except:
        return x

def try_eval(x):
    try:
        return yuno_typify(eval(x, {
            "I": sympy.I,
            "F": sympy.Rational
        }))
    except:
        return x

class compose_seq(sequence):
    def __init__(self, seq, lst, func):
        sequence.__init__(self, self._next)
        self.index = 0
        self.seq = seq
        self.lst = lst
        self.func = func
    def _next(self):
        if self.index < len(self.lst):
            val = self.func(self.lst[self.index], self.seq.next())
            self.index += 1
            return val
        return self.seq.next()

class dyad_seq(sequence):
    def __init__(self, left, right, func):
        sequence.__init__(self, self._next)
        self.index = 0
        self.left = left
        self.right = right
        self.func = func
    def _next(self):
        val = self.func(self.left[self.index], self.right[self.index])
        self.index += 1
        return val

def stringQ(lst):
    return isinstance(lst, list) and all(isinstance(x, str) for x in lst)

def vectorize(func, left = True, right = True, chop = False):
    if isinstance(left, bool): left = lambda _: left
    if isinstance(right, bool): right = lambda _: right
    def inner(*args):
        if func.arity == 0:
            return func.call()
        elif func.arity == 1:
            argument = args[0]
            if left(argument):
                if isinstance(argument, list):
                    return [inner(item) for item in argument]
                elif isinstance(argument, sequence):
                    return sequence(lambda: inner(argument.next()))
            return func.call(argument)
        else:
            larg, rarg = args
            lv = left(larg)
            rv = right(rarg)
            if lv and isinstance(larg, list):
                if rv and isinstance(rarg, list):
                    return [inner(L, R) for L, R in zip(larg, rarg)] + ([] if chop else larg[len(rarg):] + rarg[len(larg):])
                elif rv and isinstance(rarg, sequence):
                    return compose_seq(rarg, larg, inner)
                else:
                    return [inner(L, rarg) for L in larg]
            elif lv and isinstance(larg, sequence):
                if rv and isinstance(rarg, list):
                    return compose_seq(larg, rarg, lambda x, y: inner(y, x))
                elif rv and isinstance(rarg, sequence):
                    return dyad_seq(larg, rarg, inner)
                else:
                    return sequence(lambda: inner(larg.next(), rarg))
            else:
                if rv and isinstance(rarg, list):
                    return [inner(larg, R) for R in rarg]
                elif rv and isinstance(rarg, sequence):
                    return sequence(lambda: inner(larg, rarg.next()))
            return func.call(larg, rarg)
    return attrdict(arity = func.arity, call = inner)

def base250(s):
    x = 0
    for a in s:
        x = x * 250 + codepage.codepage.find(a) + 1
    return x

## NOTE - this function works identically to Jelly's `sss`
## https://github.com/DennisMitchell/jellylanguage/blob/8275dcf3f96fc42df505169712a408958a66b17c/jelly.py#L695

def decompress(string):
    result = ""
    encoded = base250(string)
    while encoded:
        encoded, mode = divmod(encoded, 3)
        if mode == 0:
            encoded, code = divmod(encoded, 96)
            result += codepage.codepage[code + 32]
        else:
            swap_case = False
            add_space = result != ""
            if mode == 2:
                encoded, flag = divmod(encoded, 3)
                swap_case = flag != 1
                add_space ^= flag != 0
            encoded, which = divmod(encoded, 2)
            curdict = dictionary.short if which else dictionary.long
            encoded, index = divmod(encoded, len(curdict))
            this = curdict[index]
            if swap_case:
                this = this[0].swapcase() + this[1:]
            if add_space:
                this = " " + this
            result += this
    return result

def output(x):
    if "m" in flags:
        try:
            x = x.evalf()
            x = eval(str(x), {"I": 1j})
        except:
            pass
    if "p" in flags:
        print(x, end = "")
    else:
        yuno_print(x)

def yuno_print(x, root = True):
    if stringQ(x):
        print(end = "".join(x))
    elif isinstance(x, list):
        if len(x) == 0 and root:
            return
        if len(x) == 1:
            return yuno_print(x[0])
        print(end = "[")
        for a in x[:-1]:
            yuno_print(a, False)
            print(end = ", ")
        yuno_print(x[-1], False)
        print(end = "]")
    elif isinstance(x, sequence):
        print(end = "{")
        index = 0
        while True:
            yuno_print(x[index])
            print(end = ", ")
            index += 1
    else:
        print(end = str(x))
