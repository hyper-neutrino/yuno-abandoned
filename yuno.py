from hi2ka import mapping as hiraganamap
from ro2ka import mapping as romajimap

import codepage, interpreter, sys

from utils import *

usage = """
yuno - a modern stack-based golfing language

$ python yuno.py <flags> <file | code> [arguments...]

Flags: h - display this help message and exit
       b - interpret code in bytecode
       B - output code in bytecode
       C - format as a CGCC submission and exit
       c - count bytes and exit
       d - output the program list right before interpretation (debug) and exit
       D - output code in bytecode as python repr
       f - read from a file
       i - when the stack is too small, input will be taken from STDIN rather than using the first argument
       m - exit math mode before outputting (remove sympy representation)
       n - output a newline
       p - print using python's string representation rather than yuno's
       s - output the stack instead of the ToS
"""

if len(sys.argv) < 3:
    raise SystemExit(usage)

_, flags, code, *arguments = sys.argv

if "h" in flags:
    raise SystemExit(usage)

if "f" in flags:
    if "b" in flags:
        with open(code, "rb") as f:
            code = "".join(codepage.codepage[x] for x in f.read())
    else:
        with open(code, "r") as f:
            code = f.read()
elif "b" in flags:
    code = "".join(codepage.codepage[ord(x)] for x in code)

arguments = list(map(try_eval, arguments))

kanamap = {**hiraganamap, **romajimap, **{x: x for x in codepage.codepage}}

replaced = []

while code:
    matches = [x for x in kanamap if code.startswith(x)]
    maxlen = max(map(len, matches), default = 0)
    filtered = [x for x in matches if len(x) == maxlen]
    if len(filtered) > 1:
        raise SystemExit(f"Multiple matches: {filtered} (this is an issue with the interpreter, not your code)")
    if filtered == []:
        if code[0] in codepage.codepage or code[0] == "\n" or code[0] == "．":
            replaced.append(code[0])
        code = code[1:]
    else:
        replaced.append(kanamap[filtered[0]])
        code = code[len(filtered[0]):]

if "C" in flags:
    if replaced:
        print(f"""# [yuno], {len(replaced)} [bytes]

    %s

[yuno]: https://github.com/hyper-neutrino/yuno
[bytes]: https://github.com/hyper-neutrino/yuno/wiki/Byte-count""" % "".join(replaced).replace("\n", "\n    "))
        raise SystemExit
    else:
        print(f"""# [yuno], {len(replaced)} [bytes]

<pre><code></code></pre>

[yuno]: https://github.com/hyper-neutrino/yuno
[bytes]: https://github.com/hyper-neutrino/yuno/wiki/Byte-count""")
    raise SystemExit

for i in range(len(replaced)):
    if replaced[i] == "．":
        replaced[i] = "。"
    if replaced[i] == "\n":
        replaced[i] = "〜"

if "c" in flags:
    print(f"{len(replaced)} bytes." + "\n\n" + "".join(f"[{x}]" for x in replaced))
    raise SystemExit

if "B" in flags:
    print("".join(map(chr, [codepage.codepage.index(x) for x in replaced])))
    raise SystemExit

if "D" in flags:
    print(repr("".join(map(chr, [codepage.codepage.index(x) for x in replaced]))))
    raise SystemExit

if replaced:
    program = interpreter.getcalls(replaced)
    if "d" in flags:
        print(program)
        raise SystemExit
    stack = interpreter.run(program, stack = arguments[::-1])
    if "s" in flags:
        print(end = "[")
        if stack:
            for x in stack[:-1]:
                output(x)
                print(end = ", ")
            output(stack[-1])
        print(end = "]")
    else:
        output(stack[-1] if stack else 0)
else:
    output(arguments[0] if arguments else 0)

if "n" in flags:
    print()
