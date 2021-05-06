# yuno
yuno, a modern procedural-ish golfing language.

To run, `python3 yuno.py <flags> <code / file> [arguments...]`. Flags are required. If you don't want any, use `python3 yuno.py "" <code / file> [arguments...]`.

## Inspirations

yuno is inspired by various stack-based languages such as Vyxal. When deciding between Jelly's tacit structure and a more conventional stack-based language, using Vyxal for just a bit convinced me to use stack-based - not only for being easier to code and to use, but because often it is just as capable for golfing as Jelly is.

## Codepage

yuno's codepage is the majority of the list of kana. The interpreter uses katakana, but hiragana is accepted, and it will also map romaji as best as it can. You can also just provide code in the raw binary (this is so the codepage, which has some three-character-wide elements, actually occupies one byte per "unit").

## Flag System

Flags are added generally only to deal with strict input/output requirements. I personally dislike challenges with inflexible I/O more than I dislike languages that abuse flags (with no reference to any specific languages made by any users on CGCC), so I implemented some flags for that purpose. However, in general, flags are only used to adapt I/O and not to move functions from the code itself into the command line.

## Type System

yuno has the following types:

- numbers
- vectors
- characters*
- sequences

Strings are just lists of characters. Specifically, if a list contains at least one element and all elements are characters, it is a string. Some functions that work on lists but don't make much sense on strings, or that would normally vectorize but don't make sense on characters, will have overloaded behavior. Some will vectorize on the characters and treat them by their codepoints. The empty list is treated as a list, since this behavior makes more sense. If you need it to work otherwise, you will likely need to find a work-around.

Vectorization will occur for most functions; specifically, mathematical functions will generally vectorize, and wherever operating on a vector seems less sensible than operating on its elements, it probably is vectorized. Some functions will only sometimes vectorize; for example, the "element of" function will first check if the left argument is in the right argument. If not, and the left argument is, it will vectorize once (this can recurse). However, if none of the results are truthy, it will revert and return the unvectorized form. Note that "element of" will not left-right vectorize; it never vectorizes on the right.
