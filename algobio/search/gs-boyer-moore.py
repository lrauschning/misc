#!/usr/bin/python3
import sys

def compute_shift_table(pattern):
    l = len(pattern)
    shift = [l for _ in range(l)]

    # sigma <= j
    border = [0 for _ in range(l + 1)]
    border[0] = -1
    i = border[1] = 0
    for j in range(2, l + 1):
        while i >= 0 and pattern[l - i - 1] != pattern[l - j]:
            sigma = j - i - 1
            shift[l - i - 1] = min(shift[l - i - 1], sigma)
            i = border[i]
        i += 1
        border[j] = i

    # sigma > j
    j = 0
    i = border[l]
    while i >= 0:
        sigma = l - i
        while j < sigma:
            shift[j] = min(shift[j], sigma)
            j += 1
        i = border[i]
    return shift


def gs_boyer_moore(text, pattern):
    comps = 0
    l = len(pattern)
    shift = compute_shift_table(pattern)
    i = 0
    j = l - 1
    while i <= len(text) - l:
        comps = comps +1 # initial loop comp
        while text[i + j] == pattern[j]:
            comps = comps +1
            if j == 0:
                return (i, comps)
            j -= 1
        i = i + shift[j]
        j = l - 1
    return (False, comps)

if (len(sys.argv) > 3 and sys.argv[3] == "bench"):
    with open(sys.argv[1]) as textf:
        with open(sys.argv[2]) as patternf:
            print(gs_boyer_moore(textf.read(), patternf.read())[1], ",", sep="", end="")
else:
    print(gs_boyer_moore(text=sys.argv[2], pattern=sys.argv[1]))
