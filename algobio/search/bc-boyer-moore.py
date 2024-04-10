#!/usr/bin/python3
import sys
from collections import defaultdict


def compute_bc_table(pattern):
    bc = defaultdict(int)
    for idx, letter in enumerate(pattern):
        if idx > bc[letter]:
            bc[letter] = idx
    return bc


def bc_boyer_moore(text, pattern):
    comps = 0
    l = len(pattern)
    i = 0
    j = l - 1
    bc = compute_bc_table(pattern)
    while i <= len(text) - l:
        comps = comps +1 # initial loop comp
        while text[i + j] == pattern[j]:
            comps = comps +1
            if j == 0:
                return (i, comps)
            j -= 1
        if text[i + j] in bc and bc[text[i + j]] < j:
            i += j - bc[text[i + j]]
            j = l - 1
        elif text[i + j] in bc and bc[text[i + j]] >= j:
            i += 1
            j = l - 1
        else:
            i += j + 1
            j = l - 1
    return (False, comps)


if (len(sys.argv) > 3 and sys.argv[3] == "bench"):
    with open(sys.argv[1]) as textf:
        with open(sys.argv[2]) as patternf:
            print(bc_boyer_moore(textf.read(), patternf.read())[1], ",", sep="", end="")
else:
    print(bc_boyer_moore(text=sys.argv[2], pattern=sys.argv[1]))
