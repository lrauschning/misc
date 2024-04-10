import string
import time

import numpy as np

from naive_string_matching import search_naive
from random_strings import get_random_string

from_ = 0
to_ = 20_000_000
step_ = 1_000_000

pattern_lengths = [100, 1_000, 10_000, 100_000]

binary = "01"
dna = "ACGT"
alphanumerical = string.digits + string.ascii_letters

found = []
print("text_length\tpattern_length\tsearch_time")
for pattern_length in pattern_lengths:
    for i in range(from_, to_ + 1, step_):
        t = []
        for _ in range(1):
            text = get_random_string(alphanumerical, i)
            pattern = get_random_string(binary, pattern_length)

            start = time.time()
            found.append(search_naive(text, pattern))
            end = time.time()
            t.append(end - start)
        print(f"{i}\t{pattern_length}\t{np.average(t)}")
# print(found.count(True))
