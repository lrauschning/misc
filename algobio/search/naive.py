#!/usr/bin/python3
import sys


def search_naive(text, pattern):
    comps = i = j = 0
    n = len(text)
    m = len(pattern)
    while i <= n - m:
        comps = comps +1 # initial loop comp
        while text[i + j] == pattern[j]:
            comps = comps +1
            j += 1
            if j == m:
                return (True, comps)
        i += 1
        j = 0
    return (False, comps)


if (len(sys.argv) > 3 and sys.argv[3] == "bench"):
    with open(sys.argv[1]) as textf:
        with open(sys.argv[2]) as patternf:
            print(search_naive(textf.read(), patternf.read())[1], ",", sep="", end="")
else:
    print(search_naive(text=sys.argv[2], pattern=sys.argv[1]))
