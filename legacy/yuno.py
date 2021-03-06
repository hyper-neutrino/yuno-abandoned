import codepage, commands, interpreter, lexer, sys

from utils import *

usage = """
yuno - a modern golfing language

$ python yuno.py <flags> <file | code> [arguments...]

Flags: h - display this help message and exit
       f - read from a file
       n - output a newline
       p - print using python's string representation rather than yuno's
"""

if len(sys.argv) < 3:
    raise SystemExit(usage)

_, flags, code, *arguments = sys.argv

if "h" in flags:
    raise SystemExit(usage)

if "f" in flags:
    with open(code, "r") as f:
        code = f.read()

arguments = list(map(try_eval, arguments))

for key, val in zip("³⁴⁵⁶⁷", arguments):
    commands.functions[key].call = Constant(val)

lines = lexer.tokenize("".join(char for char in code.replace("\n", "¶") if char in codepage.codepage))

if lines:
    interpreter.links = lines
    result = interpreter.quick_invoke(-1, *arguments[:2])
    output(result)
else:
    output(arguments[0] if arguments else 0)

if "n" in flags:
    print()
