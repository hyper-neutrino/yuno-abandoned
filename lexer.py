import codepage, commands, interpreter, re, sys

from utils import *

def base250(s):
    x = 0
    for a in s:
        x = x * 250 + codepage.codepage.find(a)
    return x

def single_eval(item):
    if item[0] == "“":
        string = [[]]
        for char in item[1:]:
            if char == "“":
                string.append([])
            elif char == "”":
                break
            elif char == "’":
                string = list(map(base250, string))
                break
            elif char == "‘":
                string = [list(map(codepage.codepage.find, line)) for line in string]
                break
            elif char == "»":
                string = [list("TODO - full compression")]
                break
            elif char == "«":
                string = [list("TODO - mixed compression")]
                break
            else:
                string[-1].append(char)
        if len(string) == 1:
            string = string[0]
        return string
    if item[0] == "”":
        return item[1]
    if item[0] == "⁽":
        val = base250(item[1:])
        return val + 1001 if val < 30800 else val - 62599
    if item[0] == "⁾":
        return list(item[1:])
    if "ı" in item:
        x, y = item.split("ı")
        return single_eval(x or "0") + 1j * single_eval(y or "1")
    if "ȷ" in item:
        x, y = item.split("ȷ")
        return single_eval(x or "1") * 10 ** single_eval(y or "3")
    if item[0] == "-":
        return -single_eval(item[1:] or "1")
    if "." in item:
        x, y = item.split(".")
        return eval((x or "0") + "." + (y or "5"))
    return eval(item)

def yuno_eval(item):
    stripped = regex_singl.sub("", item)
    return coerce(eval(regex_singl.sub(lambda m: repr(single_eval(m.group())), item) + "]" * (stripped.count("[") - stripped.count("]"))))

_re_decimal = rf"(0|-?\d*\.\d*|-?\d+|-)"
_re_realnum = rf"({_re_decimal}?ȷ{_re_decimal}?|{_re_decimal})"
_re_numbers = rf"({_re_realnum}?ı{_re_realnum}?|{_re_realnum})"

_re_intpair = rf"(⁽..)"
_re_twochar = rf"(⁾..)"
_re_charlit = rf"(”.)"
_re_fixlits = rf"({_re_intpair}|{_re_twochar}|{_re_charlit})"

_re_strlits = rf"(“[^«»‘’”]*[«»‘’”]?)"

_re_literal = rf"({_re_numbers}|{_re_fixlits}|{_re_strlits})"
_re_litlist = rf"\[*{_re_literal}((\]*,\[*){_re_literal})*\]*"

regex_singl = re.compile(_re_literal)
regex_liter = re.compile(_re_litlist)

def tokenize(code):
    lines = []
    line = []
    while code:
        if code[0] == " ":
            code = code[1:]
            continue
        if code[0] == "¶":
            if line:
                lines.append(line)
            line = []
            code = code[1:]
            continue
        match = regex_liter.match(code)
        if line == []: line = [[]]
        if match:
            group = match.group()
            line[-1].append(Constant(yuno_eval(group)))
            code = code[len(group):]
            continue
        for key, val in commands.functions.items():
            if code.startswith(key):
                line[-1].append(val)
                code = code[len(key):]
                break
        else:
            for key, val in commands.operators.items():
                if code.startswith(key):
                    line[-1].append(val(line[-1]))
                    code = code[len(key):]
                    break
            else:
                for key, val in commands.directives.items():
                    if code.startswith(key):
                        line.append([val])
                        code = code[len(key):]
                        break
                else:
                    print("Unknown character:", code[0], file = sys.stderr)
                    code = code[1:]
    if line:
        lines.append(line)
    return lines
