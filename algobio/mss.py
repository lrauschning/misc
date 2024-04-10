#!/usr/bin/python

import argparse
import io
import sys
import math
import numpy as np

## naive algorithm, implemented based on the MSS pseudocode
## in the script by Prof. Heun
## seq is the sequence to search
## feature toggles filtering for minimal/maximal length (if set to short/long). Set as None to disable.
## agg toggles agglomeration
## if there is no MSS w/ score > 0, it returns an empty subsequence/a list containing an empty subsequence, depending on if agg is set
def naive(seq, agg=False, feature="short"):
    maxscore = 0
    left = 0
    right = -1
    sel_len = 0 # used for performing the shortest/longest selection
    maxlist = [(left, right, maxscore)] # list of fitting MSS; only returned if agg is set

    for i in range(0, len(seq)):
        for j in range(i, len(seq)):
            score = sum(seq[i:j+1])
            if score > maxscore or (
                    feature == "short" and score == maxscore and j-i < sel_len
                    ) or ( feature == "long" and score == maxscore and j-i > sel_len):
                maxscore = score
                left = i
                right = j
                sel_len = j-i
                maxlist = [(left, right, maxscore)]
            elif agg and score == maxscore and (
                    not feature or j-i == sel_len): # length filtering for short/long
                maxlist.append( (i, j, score) )
    return [(left, right, maxscore)] if not agg else maxlist

## linear algorithm, implemented based on the "clever" MSS pseudocode
## in the script by Prof. Heun
## seq is the sequence to search
## feature toggles filtering for minimal/maximal length (if set to short/long). Set as None to disable.
## agg toggles agglomeration
## if there is no MSS w/ score > 0, it returns an empty subsequence/a list containing an empty subsequence, depending on if agg is set
## 
## agglomeration of all MSS (w/o filtering) is handled inline, without postprocessing:
## prefixes with score 0 are saved to a list
## suffixes are searched after finding a MSS and all combinations of pre/suffix appended to maxlist
def linear(seq, agg=False, feature="short"):
    l_maxscore = 0
    l_left = 0
    l_right = -1
    l_len = 0
    r_maxscore = 0
    r_left = 0
    maxlist = [(l_left, l_right, l_maxscore)]
    preflist = []
    for (index, value) in enumerate(seq):
        # update right candidate SMSS
        candidate = r_maxscore + value
        if candidate > value or (feature == "long" and candidate == value): # make LMSS as long as possible
            r_maxscore = candidate
        else:
            if not feature and candidate == value: # do not save prefixes for SMSS
                preflist.append(r_left)
            # reinitialise the right candidate MSS
            r_maxscore = value
            r_left = index

        # found a new [L/S]MSS
        if r_maxscore > l_maxscore or (
                feature == "short" and r_maxscore == l_maxscore and index - r_left < l_len
                ) or ( feature == "long" and r_maxscore == l_maxscore and index - r_left > l_len):
            
            # reset bookkeeping
            l_maxscore = r_maxscore
            l_left = r_left
            l_right = index
            l_len = l_right - l_left
            maxlist=[]
            # set new state
            preflist.append(l_left)
            for pref in preflist:
                maxlist.append( (pref, l_right, l_maxscore) )

            accumulator = 0
            if not feature:
                for suf in range(index+1, len(seq)):
                    accumulator = accumulator + seq[suf]
                    if accumulator == 0:
                        for pref in preflist: # append all possible combinations
                            maxlist.append( (pref, suf, l_maxscore) )
            # all prefixes have been consumed
            preflist = []
        # found another MSS
        elif agg and r_maxscore == l_maxscore and (
                not feature or index - r_left == l_len): # length filtering for short/long
            preflist.append(r_left)
            for pref in preflist:
                maxlist.append( (pref, index, l_maxscore) )

            accumulator = 0
            if not feature:
                for suf in range(index+1, len(seq)):
                    accumulator = accumulator + seq[suf]
                    if accumulator == 0:
                        for pref in preflist: # append all possible combinations
                            maxlist.append( (pref, suf, r_maxscore) )
            # all prefixes have been consumed
            preflist = []

    return [(l_left, l_right, l_maxscore)] if not agg else maxlist

## Dynamic Programming algorithm, implemented with numpy
## based on the MSS pseudocode in the script by Prof. Heun
## seq is the sequence to search
## feature toggles filtering for minimal/maximal length (if set to short/long). Set as None to disable.
## agg toggles agglomeration
## if there is no MSS w/ score > 0, it returns an empty subsequence/a list containing an empty subsequence, depending on if agg is set
def dynamic(seq, agg=False, feature="short"):
    arr = np.zeros((len(seq), len(seq)), dtype="int32")
    maxscore = 0
    left = 0
    right = -1
    sel_len = 0
    maxlist = []

    for i in range(0, len(seq)):
        for j in range(i, len(seq)):
            # if i == j, arr[i][j-1] == 0 anyway
            arr[i][j] = arr[i][j-1] + seq[j]
            if arr[i][j] > maxscore or (
                    feature == "short" and arr[i][j] == maxscore and j-i < sel_len
                    ) or ( feature == "long" and arr[i][j] == maxscore and j-i > sel_len):
                maxscore = arr[i][j]
                left = i
                right = j
                sel_len = j-i
                maxlist = [(left, right, maxscore)]
            elif agg and arr[i][j] == maxscore and (
                    not feature or j-i == sel_len): # length filtering for short/long
                maxlist.append( (i, j, arr[i][j]) )
    return [(left, right, maxscore)] if not agg else maxlist


## Divide & Conquer algorithm
## based on the MSS pseudocode in the script by Prof. Heun
# uses slices in order to be a bit more readable than manual bounds
def divide(seq, agg=False, feature="short"):
    #print("divide call, seq=", seq)
    # base case
    if(len(seq)<=1):
        return [(0, 0, seq[0])] if seq[0] > 0 else [(0, -1, 0)]
   
    m = math.floor((len(seq))/2)
    #print(m)
    # make recursive calls before assigning variables, reducing stack pollution
    l_list = divide(seq[:m])
    # the right list needs to be transformed so that its indexes correspond to this slice
    r_list = list(map(
            lambda val: (val[0] + m, val[1] + m, val[2]),
            divide(seq[m:])))

    # search for max middle solution
    ml_max = 0
    m_left = [m]
    temp = 0
    for i in range(m-1, 0, -1):
        temp = temp + seq[i]
        if temp > ml_max:
            # strict > in order to select the SMSS
            ml_max = temp
            m_left = [i]
        # expand the SMSS to a LMSS
        if feature=="long" and temp >= ml_max and i < m_left[0]:
            # ml_max does not change
            m_left = [i]
        # grab all if no feature and agg is set
        if agg and temp == ml_max:
            m_left.append(i)

    mr_max = 0
    m_right = [m]
    temp = 0
    for j in range(m+1, len(seq)):
        temp = temp + seq[j]
        if temp > mr_max:
            # strict > in order to select the SMSS
            mr_max = temp
            m_right = [j]
        # expand the SMSS to a LMSS
        if feature=="long" and temp >= ml_max and j > m_left[0]:
            # ml_max does not change
            m_right = [i]
        # grab all if no feature and agg is set
        if agg and temp == ml_max:
            m_right.append(i)
    
    m_max = ml_max + mr_max + seq[m]
    m_list = []
    for i in m_left:
        for j in m_right:
            m_list.append( (i, j, m_max) )
   
    # precompute lengths
    # contract: if a list is filtered for length, all members of the list must have the same length
    # also, all members of the list must have the same score
    l_max = l_list[0][2]
    l_len = l_list[0][1] - l_list[0][0]
    r_max = r_list[0][2]
    r_len = r_list[0][1] - r_list[0][0]
    m_len = m_list[0][1] - m_list[0][0]
    # m_max has already been calculated

    # check if a new maximum has been found
    if  l_max > r_max and l_max > m_max:
        return l_list
    if r_max > m_max:
        return r_list
    if m_max > r_max:
        return m_list

    # check if a new maximal/minimal length has been found
    if l_max >= r_max and (
        (feature == "short" and l_len < r_len)
        or (feature == "long" and l_len > r_len )):
        return l_list

    if l_max >= m_max and (
        (feature == "short" and l_len < m_len)
        or (feature == "long" and l_len > m_len )):
        return l_list

    if r_max >= m_max and (
        (feature == "short" and r_len < m_len)
        or (feature == "long" and r_len > m_len )):
        return r_list

    if m_max >= r_max and (
        (feature == "short" and m_len < r_len)
        or (feature == "long" and m_len > r_len )):
        return m_list

    # terminate if not agglomerating, saves some checks
    # choose the leftmost, as all have equal score
    if not agg:
        return l_list
    
    # agglomerating all MSS, in order
    l_list.extend(m_list)
    l_list.extend(r_list)
    return l_list


if __name__ == "__main__":
    # general arguments: i/o
    parser = argparse.ArgumentParser(description="Finds various Maximal Scoring Subsequences in a string of numbers using a variety of algorithms.")
    parser.add_argument("-i", dest="in_file", help="Input file. Default and - are stdin.", type=argparse.FileType('r'), default='-')
    parser.add_argument("-o", dest="out_file", help="Output file. Default and - are stdout.", type=argparse.FileType('w'), default='-')
    parser.add_argument("-mode", dest="mode", help="Selects which kind of MSS to search and whether to return all (aX) or only the leftmost (X).\n S: SMSS, L: LMSS, all: all MSS", type=str, choices=['S', 'aS', 'L', 'aL', 'all'], default='S')
    mode_dict = {'S': (False, "short"), 'aS': (True, "short"), 'L': (False, "long"), 'aL': (True, "long"), 'all': (True, None)}

    
    algo = parser.add_mutually_exclusive_group(required=True)
    algo.add_argument("-n", dest="func", help="Use the naive algorithm", action="store_const", const=naive)
    algo.add_argument("-l", dest="func", help="Use the Linear Programming algorithm", action="store_const", const=linear)
    algo.add_argument("-d", dest="func", help="Use the Dynamic Programming algorithm", action="store_const", const=dynamic)
    algo.add_argument("-dc", dest="func", help="Use the Divide & Conquer algorithm", action="store_const", const=divide)

    args = parser.parse_args()
    (call_agg, call_feature) = mode_dict[args.mode]
    if not args.func:
        print("You need to specify an algorithm to use!")
        sys.exit()

    # read input as comma separated list of ints
    seq = []
    try:
        seq = list(map(lambda x: int(x.strip()), args.in_file.read().split(',')))
    except:
        print("Input is not a comma-separated list of ints!")

    #print(seq)
    for mss in args.func(seq, agg=call_agg, feature=call_feature):
        args.out_file.write("\t".join(map(
            lambda x: str(x),            
            mss)))
        args.out_file.write("\n")
