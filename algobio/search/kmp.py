#!/usr/bin/python3
import sys


def compute_border(pattern):
    l = len(pattern)
    border = [0 for _ in range(l + 1)]
    border[0] = -1
    border[1] = 0
    i = border[1]
    for j in range(2, l+ 1):
        while i >= 0 and pattern[i] != pattern[j - 1]:
            i = border[i]
        i += 1
        border[j] = i
    return border


def kmp(text, pattern):
    l = len(pattern)
    border = compute_border(pattern)
    comps = i = j = 0
    while i <= len(text) - l:
        comps = comps +1 # initial loop comp
        while text[i + j] == pattern[j]:
            comps = comps +1
            j += 1
            if j == l:
                return (i, comps)
        i += j - border[j]
        j = max(0, border[j])
    return (False, comps)


if (len(sys.argv) > 3 and sys.argv[3] == "bench"):
    with open(sys.argv[1]) as textf:
        with open(sys.argv[2]) as patternf:
            print(kmp(textf.read(), patternf.read())[1], ",", sep="", end="")
else:
    print(kmp(text=sys.argv[2], pattern=sys.argv[1]))
