from hi2ka import mapping as hiraganamap
from ro2ka import mapping as romajimap

import codepage, interpreter, sys

from utils import *

usage = """
yuno - a modern stack-based golfing language

$ python yuno.py <flags> <file | code> [arguments...]

Flags: h - display this help message and exit
       b - interpret code in binary
       C - format as a CGCC submission and exit
       c - count bytes and exit
       f - read from a file
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
        raise SystemExit(f"""# [yuno], {len(replaced)} [bytes]

    %s

[yuno]: https://github.com/hyper-neutrino/yuno
[bytes]: https://github.com/hyper-neutrino/yuno/wiki/Byte-count""" % "".join(replaced).replace("\n", "\n    "))
    else:
        raise SystemExit(f"""# [yuno], {len(replaced)} [bytes]

<pre><code></code></pre>

[yuno]: https://github.com/hyper-neutrino/yuno
[bytes]: https://github.com/hyper-neutrino/yuno/wiki/Byte-count""")

for i in range(len(replaced)):
    if replaced[i] == "．":
        replaced[i] = "。"
    if replaced[i] == "\n":
        replaced[i] = "〜"

if "c" in flags:
    raise SystemExit(f"{len(replaced)} bytes." + "\n\n" + "".join(f"[{x}]" for x in replaced))

if replaced:
    program = interpreter.getcalls(replaced)
    stack = interpreter.run(program)
    if "s" in flags:
        output(stack)
    else:
        output(stack[-1] if stack else 0)
else:
    output(arguments[0] if arguments else 0)

if "n" in flags:
    print()
