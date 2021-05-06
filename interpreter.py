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
    if s[0] == "-":
        return -parsenum(s[1:])
    if "i" in s:
        x, y = s.split("i")
        return parsenum(x or "0") + sympy.I * parsenum(y or "1")
    if "j" in s:
        x, y = s.split("j")
        return parsenum(x or "1") * sympy.Rational(10) ** parsenum(y or "3")
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
        term = code[0] if code else "」"
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
        while code and (code[0] in "１２３４５６７８９０" or not dec and code[0] == "。" or not exp and code[0] == "シ" or not cmp and code[0] == "イ"):
            char = code.pop(0)
            if char in "１２３４５６７８９０":
                s += numcharmap[char]
            elif char == "。":
                dec = True
                s += "."
            elif char == "シ":
                exp = True
                dec = False
                s += "j"
            elif char == "イ":
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

def run(program, index = -1, stack = None):
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
        while len(stack) < arity:
            stack = [try_eval(input())] + stack
        if arity == 0:
            val = []
        else:
            stack, val = stack[:-arity], stack[-arity:]
        res = func(*val)
        if type(res) == tuple:
            stack += list(res)
        else:
            stack.append(res)
    return stack
