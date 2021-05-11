import math, sympy, sys

flags = sys.argv[1] if len(sys.argv) > 1 else ""

ARGS = []

def get_input():
    return try_eval(input() if "i" in flags or len(sys.argv) <= 3 else sys.argv[3])

def yuno_typify(x):
    if isinstance(x, str):
        return list(x)
    if isinstance(x, tuple):
        return list(x)
    if isinstance(x, dict):
        return list(map(list, x.items()))
    if isinstance(x, set):
        return list(x)
    if isinstance(x, int) or isinstance(x, float):
        return sympy.Number(x)
    if isinstance(x, complex):
        return sympy.Number(x.real) + x.imag * sympy.I
    return x

def arith_seq(a, d):
    a = yuno_typify(a)
    d = yuno_typify(d)
    return fseq(lambda i: a + (i - 1) * d)

def geom_seq(a, r):
    a = yuno_typify(a)
    r = yuno_typify(r)
    return fseq(lambda i: a * r ** (i - 1))

def try_eval(x):
    try:
        return yuno_typify(eval(x, {
            "I": sympy.I,
            "F": sympy.Rational,
            "P": sympy.pi,
            "E": sympy.E,
            "A": arith_seq,
            "G": geom_seq
        }))
    except:
        return x

def stringQ(lst):
    return isinstance(lst, list) and all(isinstance(x, str) for x in lst)

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

def unsympify(x):
    if isinstance(x, int) or isinstance(x, float) or isinstance(x, complex):
        return x
    return eval(str(x.evalf()), {"I": 1j})

def frange(x, y, z):
    while (z > 0 and x < y) or (z < 0 and x > y):
        yield x
        x += z

def indexinto(a, x):
    re, im = sympy.simplify(x).as_real_imag()
    if im == 0:
        if re % 1 == 0:
            return a[(int(re) - 1) % len(a)]
        return [a[(int(re) - 1) % len(a)], a[(int(math.ceil(re)) - 1) % len(a)]]
    else:
        try:
            v = [indexinto(k, im) for k in [*a, a[0]][(int(re) - 1) % len(a):][:1 + (re % 1 != 0)]]
            return v[0] if len(v) == 1 else v
        except:
            return [a[(int(i) - 1) % len(a)] if i % 1 == 0 else [a[(int(i) - 1) % a], a[(int(math.ceil(i)) - 1) % len(a)]] for i in [re, im]]

class seq:
    def __init__(self, _next):
        self._next = _next
        self.cache = []
    def __iter__(self):
        pass
    def __next__(self):
        val = self._next()
        self.cache.append(val)
        return val
    def __getitem__(self, x):
        if isinstance(x, slice):
            step = x.step or 1
            if step < 0 and x.start is None:
                raise RuntimeError("Negative step size of sequence must start at an index because infinite sequences cannot be reversed.")
            start = x.start or 1
            if x.stop is None and step > 0:
                return fseq(lambda i: self[start + (i - 1) * step])
            stop = x.stop or 0
            maxi = start if step < 0 else stop
            return [self[i] for i in frange(start, stop, step)]
        re, im = sympy.Number(x).as_real_imag()
        b = math.ceil(max(re, im))
        while len(self.cache) <= b:
            self.__next__()
        return indexinto(self.cache, x)
    def __len__(self):
        return float("inf")

class fseq(seq):
    def __init__(self, _map):
        seq.__init__(self, None)
        self._map = _map
        self.index = 1
    def __iter__(self):
        self.index = 1
    def __next__(self):
        val = self._map(self.index)
        self.index += 1
        self.cache.append(val)
        return val

def vecm(func, obj, xcond = False):
    recur = lambda o: vecm(func, o, xcond)
    if xcond in [True, False]:
        xcond = (lambda xcond: lambda _: xcond)(xcond)
    if xcond(obj) or not isinstance(obj, list) and not isinstance(obj, seq):
        return func(obj)
    if isinstance(obj, list):
        return [vecm(func, item, xcond) for item in obj]
    if isinstance(obj, seq):
        return fseq(lambda i: recur(obj[i]))

sqvecd = lambda f: lambda x, y: vecd(f, x, y, stringQ, stringQ)

def vecd(func, larg, rarg, xlcond = False, xrcond = False):
    recur = lambda l, r: vecd(func, l, r, xlcond, xrcond)
    if xlcond in [True, False]:
        xlcond = (lambda xlcond: lambda _: xlcond)(xlcond)
    if xrcond in [True, False]:
        xrcond = (lambda xrcond: lambda _: xrcond)(xrcond)
    lxvec = xlcond(larg) or not isinstance(larg, list) and not isinstance(larg, seq)
    rxvec = xrcond(rarg) or not isinstance(rarg, list) and not isinstance(rarg, seq)
    if lxvec:
        if rxvec:
            return func(larg, rarg)
        if isinstance(rarg, list):
            return [recur(larg, r) for r in rarg]
        if isinstance(rarg, seq):
            return fseq(lambda i: recur(larg, rarg[i]))
    if isinstance(larg, list):
        if rxvec:
            return [recur(l, rarg) for l in larg]
        if isinstance(rarg, list):
            return [recur(l, r) for l, r in zip(larg, rarg)] + rarg[len(larg):] + larg[len(rarg):]
        if isinstance(rarg, seq):
            return fseq(lambda i: recur(larg[i - 1], rarg[i]) if i <= len(larg) else rarg[i])
    if isinstance(larg, seq):
        if rxvec:
            return fseq(lambda i: recur(larg[i], rarg))
        if isinstance(rarg, list):
            return fseq(lambda i: recur(larg[i], rarg[i - 1]) if i <= len(rarg) else larg[i])
        if isinstance(rarg, seq):
            return fseq(lambda i: recur(larg[i], rarg[i]))

def unmath(x):
    if isinstance(x, list):
        return list(map(unmath, x))
    if isinstance(x, seq):
        return fseq(lambda i: unmath(x[i]))
    try:
        return unsympify(x)
    except:
        return x

def output(x):
    if "m" in flags:
        x = unmath(x)
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
    elif isinstance(x, seq):
        print(end = "{")
        index = 0
        while True:
            yuno_print(x[index])
            print(end = ", ")
            index += 1
    else:
        print(end = str(x))
