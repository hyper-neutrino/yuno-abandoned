import itertools, sympy

from codepage import codepage
from ka2sym import mapping as kanamap

from utils import *

GLOBAL_REGISTER = 0

skanalist = [x for x in codepage if x not in "」アエイオ"]

numcharmap = {
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
    "６": "6",
    "７": "7",
    "８": "8",
    "９": "9",
    "０": "0",
    "ー": "-",
    "。": ".",
    "イ": "i",
    "シ": "j"
}

def const(x):
    return lambda: x

def parsenum(s):
    if "," in s:
        return list(map(parsenum, s.split(",")))
    if "i" in s:
        x, y = s.split("i")
        return parsenum(x or "0") + sympy.I * parsenum(y or "1")
    if "j" in s:
        x, y = s.split("j")
        return parsenum(x or "1") * sympy.Rational(10) ** parsenum(y or "3")
    if s[0] == "-":
        return -parsenum(s[1:] or "1")
    if "." in s:
        x, y = s.split(".")
        s = (x or "0") + "." + (y or "5")
    return sympy.Rational(s)

def getcalls(code):
    result = [[]]
    while code:
        if code[0] == "〜":
            code.pop(0)
            result.append([])
            continue
        call = getcall(code)
        if call is not None:
            result[-1].append(call)
    return result

def split(a, x, sub = False):
    a, x = listnumord(a, x, listdigits)
    if not sub:
        x = [x]
    xl = len(x)
    if isinstance(a, seq):
        class splitseq(seq):
            def __init__(self, pseq, psplit):
                seq.__init__(self, None)
                self.pseq = pseq
                self.psplit = psplit
                self.psl = len(psplit)
                self.index = 1
            def __iter__(self):
                self.index = 1
            def __next__(self):
                result = []
                while self.pseq[self.index:self.index + self.psl] != self.psplit:
                    result.append(self.pseq[self.index])
                    self.index += 1
                self.index += self.psl
                self.cache.append(result)
                return result
        return splitseq(a, x)
    results = [[]]
    i = 0
    while i < len(a):
        if a[i:i + xl] == x:
            results.append([])
            i += xl
        else:
            results[-1].append(a[i])
            i += 1
    return results

def stringify(x):
    if stringQ(x):
        return "".join(x)
    else:
        return str(x)

def anystr(*x):
    return any(isinstance(q, str) or stringQ(q) for q in x)

def getfun(code):
    result = []
    while code and code[0] not in ["〜", "；"]:
        call = getcall(code)
        if call is not None:
            result.append(call)
    if code:
        code.pop(0)
    return result

def yrange(x, lo, hi):
    if isinstance(x, str):
        x = sympy.Number(ord(x))
    re, im = x.as_real_imag()
    if re > 0:
        main = list(map(sympy.Number, range(lo, int(re) + hi)))
    else:
        main = list(map(sympy.Number, range(lo - 1, int(sympy.ceiling(re)) - hi, -1)))
    if im == 0:
        return main
    else:
        if im > 0:
            dim = list(map(sympy.Number, range(int(im) + 1)))
        else:
            dim = list(map(sympy.Number, range(0, int(sympy.ceiling(im)) - 1, -1)))
        return [[x + y * sympy.I for y in dim] for x in main]

def ispyiter(x):
    return isinstance(x, list) or isinstance(x, tuple) or isinstance(x, set) or isinstance(x, dict)

def isiter(x):
    return isinstance(x, list) or isinstance(x, seq)

def listrange(x):
    return listcoerce(x) if ispyiter(x) else yrange(x, 1, 1)

def listwrap(x):
    return listcoerce(x) if ispyiter(x) else [x]

def listdigits(x):
    return listcoerce(x) if ispyiter(x) else list(map(int, str(x))) if x % 1 == 0 else list(str(x))

def listcoerce(x):
    return list(x) if ispyiter(x) and not isinstance(x, list) else x

def listnumord(x, y, autolist = lambda x: x):
    if not isiter(x) and isiter(y):
        return (y, x)
    if not isiter(x):
        return (autolist(x), y)
    return (x, y)

def getnextcall(code):
    call = None
    while call is None:
        call = getcall(code)
    return call

def frombase(digits, base):
    tot = sympy.Number(0)
    for x in digits[::-1]:
        tot *= base
        tot += x
    return tot

def getcall(code):
    char = code.pop(0)
    if char == "　":
        return None
    elif char == "「":
        slist = [[]]
        while code and code[0] not in "」アエイオ":
            if code[0] == "「":
                slist.append([])
            else:
                slist[-1].append(code[0])
            code.pop(0)
        term = code.pop(0) if code else "」"
        if term == "」":
            slist = [list("".join([kanamap[x] for x in row])) for row in slist]
        elif term == "ア":
            slist = [[skanalist.index(x) for x in row] for row in slist]
        elif term == "エ":
            slist = [list("".join(x)) for x in slist]
        elif term == "オ":
            slist = [frombase([skanalist.index(x) for x in row], 250) for row in slist]
        else:
            slist = ["TODO - string ending with " + term]
        if len(slist) == 1:
            slist = slist[0]
        return (0, const(slist))
    elif char in "１２３４５６７８９０。イシー":
        neg = char == "ー"
        dec = False
        exp = False
        cmp = False
        s = numcharmap[char]
        while code and (code[0] in "１２３４５６７８９０" or \
                           not dec and code[0] == "。" or \
                           not exp and code[0] == "シ" or \
                           not cmp and code[0] == "イ" or \
                           not neg and code[0] == "ー" or \
                           code[0] == "、" and len(code) > 1 and code[1] in "１２３４５６７８９０。イシー"):
            char = code.pop(0)
            if char in "１２３４５６７８９０":
                s += numcharmap[char]
            elif char == "、":
                neg = dec = exp = cmp = False
                s += ","
            elif char == "。":
                dec = True
                s += "."
            elif char == "ー":
                neg = True
                s += "-"
            elif char == "シ":
                neg = False
                exp = True
                dec = False
                s += "j"
            elif char == "イ":
                neg = False
                cmp = True
                exp = False
                dec = False
                s += "i"
        return (0, const(parsenum(s)))
    elif char == "」":
        if code:
            char = kanamap[code.pop(0)]
        else:
            char = " "
        return (0, const(char))
    elif char == "カ":
        if code:
            char = code.pop(0)
        else:
            char = "　"
        return (0, const(char))
    elif char == "ア":
        def add(x, y):
            if anystr(x, y):
                return list(stringify(x) + stringify(y))
            return x + y
        return (2, sqvecd(add))
    elif char == "ミ":
        def sub(x, y):
            if stringQ(x) or stringQ(y) or isinstance(x, str) or isinstance(y, str):
                raise SystemExit("No implementation for subtracting strings yet.")
            return x - y
        return (2, sqvecd(sub))
    elif char == "ム":
        def mul(x, y):
            if anystr(x, y):
                raise SystemExit("No implementation for multiplying strings yet (use repetition).")
            return x * y
        return (2, sqvecd(mul))
    elif char == "ディ":
        def tdiv(x, y):
            if anystr(x, y):
                raise SystemExit("No implementation for true-dividing strings yet (use list cutting).")
            if y == 0:
                return sympy.Number(0)
            return x / y
        return (2, sqvecd(tdiv))
    elif char == "ヂ":
        def fdiv(x, y):
            if anystr(x, y):
                raise SystemExit("No implementation for floor-dividing strings yet (use list cutting).")
            if y == 0:
                return sympy.Number(0)
            return x // y
        return (2, sqvecd(fdiv))
    elif char == "％":
        def modulo(x, y):
            if anystr(x, y):
                raise SystemExit("No implementation for modulo on strings yet.")
            if y == 0:
                return sympy.Number(0)
            return x % y
        return (2, sqvecd(modulo))
    elif char == "ラ":
        return (1, lambda x: vecm(lambda y: yrange(y, 1, 1), x))
    elif char == "レ":
        return (1, lambda x: vecm(lambda y: yrange(y, 0, 1), x))
    elif char == "リ":
        return (1, lambda x: vecm(lambda y: yrange(y, 1, 0), x))
    elif char == "ロ":
        return (1, lambda x: vecm(lambda y: yrange(y, 0, 0), x))
    elif char == "ン":
        return (1, lambda x: vecm(lambda y: y + 1, x))
    elif char == "デ":
        return (1, lambda x: vecm(lambda y: y - 1, x))
    elif char == "コ":
        arity, func = getnextcall(code)
        def handle(*a):
            a = list(a)
            re, im = a[0].as_real_imag()
            a[0] = im
            out = run(_program, _index, a, [(arity, func)])
            return tuple(re + x * sympy.I for x in out)
        return (arity, handle)
    elif char == "＄":
        a1, f1 = getnextcall(code)
        a2, f2 = getnextcall(code)
        return (a1, lambda *a: (lambda b: f2(*(b[-a2:] if a2 != -1 else b)))(listwrap(f1(*a))))
    elif char == "ネ":
        return (1, lambda x: vecm(lambda y: y.swapcase() if isinstance(y, str) else -y, x))
    elif char == "マ":
        arity, func = getnextcall(code)
        def handle(*a):
            a = list(a)
            if isinstance(a[0], seq):
                return fseq(lambda i: run(_program, _index, [a[0][i], *a[1:]], [(arity, func)]))
            if not isinstance(a[0], list):
                a[0] = yrange(a[0], 1, 1)
            return [listcoerce(run(_program, _index, [q, *a[1:]], [(arity, func)])) for q in a[0]]
        return (arity, handle)
    elif char == "メ":
        arity, func = getnextcall(code)
        def handle(*a):
            a = list(a)
            if isinstance(a[1], seq):
                return fseq(lambda i: run(_program, _index, [a[0], a[1][i], *a[2:]], [(arity, func)]))
            if not isinstance(a[1], list):
                a[1] = yrange(a[1], 1, 1)
            return [listcoerce(run(_program, _index, [a[0], q, *a[2:]], [(arity, func)])) for q in a[1]]
        return (arity, handle)
    elif char == "ヌ":
        return (1, lambda x: vecm(lambda k: len(k) if isinstance(k, list) or isinstance(k, str) else len(str(k).replace(" ", "")), x, lambda k: not isinstance(k, seq)))
    elif char == "ッキャ":
        return (-1, lambda *a: tuple(run(_program, _index, list(a))))
    elif char == "ッキョ":
        return (-1, lambda *a: tuple(run(_program, _index - 1, list(a))))
    elif char == "ッキュ":
        return (-1, lambda *a: tuple(run(_program, _index + 1, list(a))))
    elif char == "？":
        a1, f1 = getnextcall(code)
        a2, f2 = getnextcall(code)
        a3, f3 = getnextcall(code)
        def handle(*a):
            stack = list(a)
            res = listwrap(run(_program, _index, stack[:], [(a1, f1)]))[-1]
            return tuple(run(_program, _index, stack, [(a2, f2) if res else (a3, f3)]))
        return (-1, handle)
    elif char == "フ":
        fs = []
        while code and code[0] != "；":
            call = getcall(code)
            if call is not None:
                fs.append(call)
        if code:
            code.pop(0)
        return (fs[0][0] if fs else arity, lambda *a: tuple(listwrap(run(_program, _index, list(a), fs))))
    elif char == "モ":
        code.insert(0, "マ")
        code.insert(1, "フ")
        return None
    elif char == "、":
        return (2, lambda a, b: [a, b])
    elif char == "ップ":
        code.insert(0, "メ")
        code.insert(1, "マ")
        return None
    elif char == "ｒ":
        return (0, lambda: GLOBAL_REGISTER)
    elif char == "Ｒ":
        def setreg(x):
            global GLOBAL_REGISTER
            GLOBAL_REGISTER = x
            return x
        return (1, setreg)
    elif char == "ル":
        a1, f1 = getnextcall(code)
        def handle():
            global GLOBAL_REGISTER
            stack = [GLOBAL_REGISTER]
            GLOBAL_REGISTER = (listwrap(run(_program, _index, stack, [(a1, f1)])) or [sympy.Number(0)])[-1]
            return ()
        return (0, handle)
    elif char == "ドゥ":
        return (1, lambda a: (a, a))
    elif char == "＠":
        return (2, lambda a, b: (b, a))
    elif char == "パ":
        return (2, lambda a, b: listwrap(a) + listwrap(b))
    elif char == "タ":
        return (2, lambda a, b: listwrap(b) + listwrap(a))
    elif char == "ス":
        return (2, split)
    elif char == "ッス":
        return (2, lambda x, y: split(x, y, True))
    elif char == "ッパ":
        def prefixes(a):
            if isinstance(a, list):
                return [a[:i] for i in range(len(a) + 1)]
            elif isinstance(a, seq):
                return fseq(lambda i: a[:i])
            else:
                return prefixes(yrange(a, 1, 1))
        return (1, prefixes)
    elif char == "ッペ":
        def permutations(a):
            return list(map(list, itertools.permutations(a)))
        return (1, permutations)
    elif char == "ヴェ":
        arity, func = getnextcall(code)
        def handle(*a):
            a = list(map(listrange, a))
            return [func(*x) for x in zip(*a)]
        return (arity, handle)
    elif char == "ジ":
        return (1, lambda a: (lambda q: [[k[i] for k in a] for i in range(q)])(max(map(len, a))))
    elif char == "ッタ":
        return (2, lambda a, b: (lambda x, y: vecm(lambda q: x[q - 1:], y))(*listnumord(a, b, listrange)))
    elif char == "ヘ":
        return (2, lambda a, b: (lambda x, y: vecm(lambda q: x[:q], y))(*listnumord(a, b, listrange)))
    elif char == "ジョ":
        def join(a, b):
            a, b = listnumord(a, b, listrange)
            b = listwrap(b)
            if isinstance(a, list):
                if not a:
                    return []
                res = []
                for x in a[:-1]:
                    res += listwrap(x)
                    res += b[:]
                return res + listwrap(a[-1])
            elif isinstance(a, seq):
                class joinseq(seq):
                    def __init__(self, pseq, joiner):
                        seq.__init__(self, None)
                        self.pseq = pseq
                        self.joiner = joiner
                        self.queue = []
                        self.psindex = 1
                    def __iter__(self):
                        self.queue = []
                        self.psindex = 1
                    def __next__(self):
                        while not self.queue:
                            self.queue.extend(listwrap(self.pseq[self.psindex]))
                            self.queue.extend(self.joiner)
                            self.psindex += 1
                        val = self.queue.pop(0)
                        self.cache.append(val)
                        return val
                return joinseq(a, b)
        return (2, join)
    elif char == "ソ":
        return (1, lambda x: vecm(sorted, listdigits(x), lambda q: isinstance(q, list)))
    elif char == "リャ":
        return (2, lambda a, b: vecd(lambda x, y: x[-(y % len(x)):] + x[:-(y % len(x))], *listnumord(a, b, listrange), lambda x: isinstance(x, list)))
    elif char == "リョ":
        return (2, lambda a, b: vecd(lambda x, y: x[(y % len(x)):] + x[:(y % len(x))], *listnumord(a, b, listrange), lambda x: isinstance(x, list)))
    elif char == "ッシュ":
        def sublists(a):
            if not isiter(a):
                a = listrange(a)
            if isinstance(a, list):
                results = []
                for length in range(1, len(a) + 1):
                    for start in range(len(a) - length + 1):
                        results.append(a[start:start + length])
                return results
            elif isinstance(a, seq):
                class subseq(seq):
                    def __init__(self, pseq):
                        seq.__init__(self, None)
                        self.pseq = pseq
                        self.queue = [[]]
                        self.qi = 1
                        self.vi = 1
                    def __iter__(self):
                        self.queue = [[]]
                        self.qi = 1
                        self.vi = 1
                    def __next__(self):
                        if self.qi >= len(self.queue):
                            self.queue.extend([[*x, self.pseq[self.vi]] for x in self.queue])
                            self.vi += 1
                        val = self.queue[self.qi]
                        self.qi += 1
                        self.cache.append(val)
                        return val
                return subseq(a)
        return (1, sublists)
    elif char == "フィ":
        arity, func = getnextcall(code)
        def handle(*a):
            a = list(a)
            if isinstance(a[0], seq):
                return filterseq(a[0], lambda x: run(_program, _index, [x, *a[1:]], [(arity, func)]))
            if not isinstance(a[0], list):
                a[0] = yrange(a[0], 1, 1)
            return [q for q in a[0] if (run(_program, _index, [q, *a[1:]], [(arity, func)]) or [0])[-1]]
        return (arity, handle)
    elif char == "フェ":
        code.insert(0, "フィ")
        code.insert(1, "フ")
        return None
    elif char == "ビ":
        return (1, lambda x: vecm(lambda y: y % 2, x))
    elif char == "ッコ":
        def count(x, y):
            if isinstance(y, seq):
                return fseq(lambda i: count(x, y[i]))
            return x.count(y)
        return (2, lambda x, y: (lambda a, b: vecm(lambda q: count(q, b), a, lambda v: isinstance(v, list)))(*listnumord(x, y, listdigits)))
    elif char == "ッキ":
        def recursivecount(x, y):
            if isinstance(y, seq):
                return fseq(lambda i: recursivecount(x, y[i]))
            normcount = x.count(y)
            if normcount == 0 and isinstance(y, list):
                subcounts = [recursivecount(x, b) for b in y]
                if any(subcounts):
                    return subcounts
            return normcount
        return (2, lambda x, y: (lambda a, b: vecm(lambda q: recursivecount(q, b), a, lambda v: isinstance(v, list)))(*listnumord(x, y, listdigits)))
    elif char == "イェ":
        return (1, lambda x: x)
    elif char == "ッカ":
        def allequal(x):
            x = listdigits(x)
            return sympy.Number(all(y == x[0] for y in x[1:])) if x else sympy.Number(1)
        return (1, allequal)
    elif char == "ハ":
        return (1, lambda x: listdigits(x)[0])
    elif char == "テ":
        return (1, lambda x: listdigits(x)[-1])
    elif char == "プ":
        return (1, lambda x: output(x) or x)
    elif char == "リュ":
        return (2, lambda x, y: (lambda a, b: vecd(lambda q, r: q * r, a, b, lambda v: isinstance(v, list)))(*listnumord(x, y, listwrap)))

def run(program, index = -1, stack = None, override = None):
    global _program, _index, _stack, _override
    index %= len(program)
    code = override or program[index]
    if stack is None:
        stack = []
    stack = list(stack)
    for arity, func in code:
        _program = [*program[:index], code, *program[index + 1:]]
        _index = index
        _stack = stack
        _override = override
        while len(stack) < arity:
            stack = [get_input()] + stack
        if arity == 0:
            val = []
        elif arity == -1:
            stack, val = [], stack
        else:
            stack, val = stack[:-arity], stack[-arity:]
        res = func(*val)
        if type(res) == tuple:
            stack += list(map(simpl, res))
        else:
            stack.append(simpl(res))
    return stack

def simpl(r):
    if isinstance(r, list):
        return list(map(simpl, r))
    if isinstance(r, seq):
        return fseq(lambda i: simpl(r[i]))
    if isinstance(r, str):
        return r
    try:
        return sympy.simplify(r)
    except:
        return r
