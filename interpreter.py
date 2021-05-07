import sympy

from codepage import codepage
from ka2sym import mapping as kanamap

from utils import *

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
        while code and (code[0] in "１２３４５６７８９０" or not dec and code[0] == "。" or not exp and code[0] == "シ" or not cmp and code[0] == "イ" or not neg and code[0] == "ー"):
            char = code.pop(0)
            if char in "１２３４５６７８９０":
                s += numcharmap[char]
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
    elif char == "ラ":
        return (1, lambda x: vecm(lambda y: yrange(y, 1, 1), x))
    elif char == "レ":
        return (1, lambda x: vecm(lambda y: yrange(y, 0, 1), x))
    elif char == "リ":
        return (1, lambda x: vecm(lambda y: yrange(y, 1, 0), x))
    elif char == "ロ":
        return (1, lambda x: vecm(lambda y: yrange(y, 0, 0), x))

def run(program, index = -1, stack = None, override = None):
    code = override or program[index % len(program)]
    if stack is None:
        stack = []
    for arity, func in program[index % len(program)]:
        if arity == -1:
            offset, arity = func
            func = lambda *a: tuple(run(program, index + offset, list(a)))
        elif arity == -2:
            newindex, arity = func
            func = lambda *a: tuple(run(program, newindex, list(a)))
        elif arity == -3:
            arity = len(stack)
        elif arity == -4:
            arity, func = func
            func = (lambda func: lambda *a: tuple(run(program, index, list(a), func)))(func)
        while len(stack) < arity:
            stack = [try_eval(input())] + stack
        if arity == 0:
            val = []
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
    try:
        return sympy.simplify(r)
    except:
        return r
