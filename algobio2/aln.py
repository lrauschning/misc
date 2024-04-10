#!/bin/python

d_match = 0
d_mismatch = 1
d_gap = 2


# implement the simplified Needleman-Wunsch algorithm for linear gap costs
def aln (seq1, seq2):
    len1 = len(seq1)
    len2 = len(seq2)

    # initialise the DP matrix; first is score, second backtrace value
    # backtrace: 0 -> match, >0 -> insertion, <0 -> gap in seq1
    arr = [ [(0, 0) for i in seq1] for c in seq2]

    for i in range(1, len1):
        arr[0][i]=(d_gap*i, 1)

    for j in range(1, len2):
        arr[j][0]=(d_gap*j, -1)

    # fill in the DP matrix
    for i in range(1, len1):
        for j in range(1, len2):
            mat = (arr[j-1][i-1][0] + d_match\
                    if seq1[i] == seq2[j]\
                    else arr[j-1][i-1][0] + d_mismatch, 0)
            ins = (arr[j-1][i][0] + d_gap, -1)
            gap = (arr[j][i-1][0] + d_gap, 1)
            arr[j][i] = min(mat, ins, gap)
    
    # backtrace
    ret1 = ""
    ret2 = ""
    #print(arr)

    i = len1-1
    j = len2-1
    while i >= 0 or j >= 0:
        if arr[j][i][1] == 0: # match
            ret1 += seq1[i]
            ret2 += seq2[j]
            i -= 1
            j -= 1
        elif arr[j][i][1] > 0: # insertion
            ret1 += seq1[i]
            ret2 += '-'
            i -= 1
        elif arr[j][i][1] < 0: # gap
            ret1 += '-'
            ret2 += seq2[j]
            j -= 1
    
    return (ret1[::-1], ret2[::-1])





if __name__ == "__main__":
    import sys
    print(aln(sys.argv[1], sys.argv[2]))
