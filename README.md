# yuno
yuno, a modern procedural-ish golfing language.

## Type System

yuno has the following types:

- numbers
- vectors
- characters
- sequences

Currently, the following sequences are supported:

- arithmetic sequences
- geometric sequences
- repeating sequences
- recursively defined sequences
- series of any sequence (including series)
- sequences formed via vectorization / mapping over existing sequences

Vectorization will occur for most functions; specifically, mathematical functions will generally vectorize, and wherever operating on a vector seems less sensible than operating on its elements, it probably is vectorized. Some functions will only sometimes vectorize; for example, the "element of" function will first check if the left argument is in the right argument. If not, and the left argument is, it will vectorize once (this can recurse). However, if none of the results are truthy, it will revert and return the unvectorized form. Note that "element of" will not left-right vectorize; it never vectorizes on the right.

Strings are not real in yuno. They are simply lists of characters (where each character is technically a Python string with just one character).
