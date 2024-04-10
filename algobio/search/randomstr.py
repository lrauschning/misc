#!/usr/bin/python3
import random
import sys

def get_random_string(alphabet: str, length: int):
    return "".join(random.choices(alphabet, k=length))

alphabets = {"dna":"ACGT", "bin":"01", "alnum":"0123456789abcdefghijklmnopqrstvwxyzABCDEFGHIJKLMNOPQRSTVWXYZ"}
print(get_random_string(alphabets[sys.argv[1]], int(sys.argv[2])))
