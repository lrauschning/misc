#!/usr/bin/python

import argparse
import io
import sys
import math
import numpy as np

## naive algorithm, implemented based on the MSS pseudocode
## in the script by Prof. Heun
## seq is the sequence to search
def naive(seq):
    maxscore = 0
    left = 0
    right = -1
    sel_len = 0 # used for performing the shortest/longest selection

    for i in range(0, len(seq)):
        for j in range(i, len(seq)):
            score = sum(seq[i:j+1])
            if score > maxscore or (score == maxscore and j-i < sel_len):
                maxscore = score
                left = i
                right = j
                sel_len = j-i
    return (left, right, maxscore)

## linear algorithm, implemented based on the "clever" MSS pseudocode
## in the script by Prof. Heun
## seq is the sequence to search
def linear(seq):
    l_maxscore = 0
    l_left = 0
    l_right = -1
    l_len = 0
    r_maxscore = 0
    r_left = 0
    for (index, value) in enumerate(seq):
        # update right candidate SMSS
        candidate = r_maxscore + value
        if candidate > value: # actually select the shortest MSS
            r_maxscore = candidate
        else:
            # reinitialise the right candidate MSS
            r_maxscore = value
            r_left = index

        # found a new [L/S]MSS
        if r_maxscore > l_maxscore or (
                r_maxscore == l_maxscore and index - r_left < l_len):

            # reset bookkeeping
            l_maxscore = r_maxscore
            l_left = r_left
            l_right = index
            l_len = l_right - l_left

    return (l_left, l_right, l_maxscore)

## Dynamic Programming algorithm, implemented with numpy
## based on the MSS pseudocode in the script by Prof. Heun
## seq is the sequence to search
def dynamic(seq):
    arr = np.zeros((len(seq), len(seq)), dtype="int32")
    maxscore = 0
    left = 0
    right = -1
    sel_len = 0

    for i in range(0, len(seq)):
        for j in range(i, len(seq)):
            # if i == j, arr[i][j-1] == 0 anyway
            arr[i][j] = arr[i][j-1] + seq[j]
            if arr[i][j] > maxscore or (
                    arr[i][j] == maxscore and j-i < sel_len):
                maxscore = arr[i][j]
                left = i
                right = j
                sel_len = j-i
    return (left, right, maxscore)


## Divide & Conquer algorithm
## based on the MSS pseudocode in the script by Prof. Heun
# uses slices in order to be a bit more readable than manual bounds
def divide(seq):
    #print("divide call, seq=", seq)
    # base case
    if(len(seq)<=1):
        return (0, 0, seq[0]) if seq[0] > 0 else (0, -1, 0)
   
    m = math.floor((len(seq))/2)
    #print(m)
    # make recursive calls before assigning variables, reducing stack pollution
    (l_left, l_right, l_max) = divide(seq[:m])
    (r_left, r_right, r_max) = divide(seq[m:])
    # adjust index
    r_left = r_left + m
    r_right = r_right + m

    # search for max middle solution
    ml_max = 0
    m_left = m
    temp = 0
    for i in range(m-1, 0, -1):
        temp = temp + seq[i]
        if temp > ml_max: # strict > in order to actually select the SMSS
            ml_max = temp
            m_left = i

    mr_max = 0
    m_right = m
    temp = 0
    for j in range(m+1, len(seq)):
        temp = temp + seq[j]
        if temp > mr_max: # strict > in order to actually select the SMSS
            mr_max = temp
            m_right = j

    m_max = ml_max + mr_max + seq[m]
   
    # check if a new maximum has been found
    if  l_max > r_max and l_max > m_max:
        return (l_left, l_right, l_max)
    if m_max > r_max:
        return (m_left, m_right, m_max)
    if r_max > m_max:
        return (r_left, r_right, r_max)

    # all MSS must be of equal score now
    # precompute lengths
    l_len = l_right - l_left
    m_len = m_right - m_left
    r_len = r_right - r_left

    if l_len < r_len and l_len < m_len:
        return (l_left, l_right, l_max)
    if m_len < r_len:
        return (m_left, m_right, m_max)
    if r_len < m_len:
        return (r_left, r_right, r_max)

    # all else being equal, return the leftmost SMSS
    return (l_left, l_right, l_max)



if __name__ == "__main__":
    # general arguments: i/o
    parser = argparse.ArgumentParser(description="Finds various Maximal Scoring Subsequences in a string of numbers using a variety of algorithms.")
    parser.add_argument("-i", dest="in_file", help="Input file. Default and - are stdin.", type=argparse.FileType('r'), default='-')
    parser.add_argument("-o", dest="out_file", help="Output file. Default and - are stdout.", type=argparse.FileType('w'), default='-')

    
    algo = parser.add_mutually_exclusive_group(required=True)
    algo.add_argument("-n", dest="func", help="Use the naive algorithm", action="store_const", const=naive)
    algo.add_argument("-l", dest="func", help="Use the Linear Programming algorithm", action="store_const", const=linear)
    algo.add_argument("-d", dest="func", help="Use the Dynamic Programming algorithm", action="store_const", const=dynamic)
    algo.add_argument("-dc", dest="func", help="Use the Divide & Conquer algorithm", action="store_const", const=divide)

    args = parser.parse_args()
    if not args.func:
        print("You need to specify an algorithm to use!")
        sys.exit()

    # read input as comma separated list of ints
    try:
        seq = list(map(lambda x: int(x.strip()), args.in_file.read().split(',')))
    except:
        print("Input is not a comma-separated list of ints!")

    #print(seq)
    #print("calling ", args.func)
    args.out_file.write("\t".join(
            map(lambda x: str(x), args.func(seq)))
            )
    args.out_file.write("\n")
