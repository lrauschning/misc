#!/bin/python
import sys

### This is quite possibly the ugliest implementation of the Needleman-Wunsch algorithm known to mankind.

def print_smartly(x):
    for l in x:
        print(l)

sequence = []
with open(sys.argv[1], 'r') as f:
    sequence = list(map(int, f.read().split(",")))

#print(sequence)

n = sum(sequence)
if n %2 ==1:
    print("No partition possible!")
    sys.exit(-1)

col1 = int(n/2)+1
col2 = len(sequence)+1


# initialise the DP matrix
# first index is sum of partition, second index in sequence
dp = [ [(0,0) for i in range(0, col2)] for s in range(0, col1)]

for s in range(0, col1):
    dp[s][0] = (-1, -1)
dp[0] = [(i,0) for i in range(0,col2)]

#print_smartly(dp)
# fill the dp matrix w/ backtraces
for s in range(1, col1):
    dp[s][1:]=[(s-val, i-1) if s-val >= 0 and not dp[s-val][i-1] == (-1,-1) else
                (s, i-1) if not dp[s][i-1] == (-1,-1)
                else (-1,-1) # encodes FALSE
            for i, val in enumerate(sequence, 1)]

#print_smartly(dp)

# error handling
if dp[col1-1][col2-1] == (-1, -1):
    print("No partition possible!")
    sys.exit(-1)


# construct the solution by backtracking
part1 = []
part2 = sequence.copy()
ind1 = col1-1
ind2 = col2-1
while ind2 > 0:
    new1, new2 = dp[ind1][ind2]
    if new1 == ind1-sequence[ind2-1]:
        #print("appending", sequence[ind2-1], "at", ind2)
        part1.append(sequence[ind2-1])
        part2[ind2-1] = None
    (ind1, ind2) = (new1, new2)

# sort and remove deleted entries
part1.sort()
part2 = list(filter(lambda x: x is not None, part2))
part2.sort()

print(part1, ", Σ =", sum(part1))
print(part2, ", Σ =", sum(part2))
