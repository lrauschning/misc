#!/bin/python

import sys
import random
import time
import os

## do console init & error handling
fallbackscript = """
SET msgboxTitle=ERROR
SET msgboxBody=IN ORDER TO USE THIS SCRIPT, YOU NEED A PROPER OS (https://www.gentoo.org/downloads/)
SET tmpmsgbox=%temp%\~tmpmsgbox.vbs
IF EXIST "%tmpmsgbox%" DEL /F /Q "%tmpmsgbox%"
ECHO msgbox "%msgboxBody%",0,"%msgboxTitle%">"%tmpmsgbox%"
WSCRIPT "%tmpmsgbox%"
"""

os.system(fallbackscript if os.name == 'nt' else 'clear')
if os.name == 'nt':
    time.sleep(60)
    raise OSError("It's not a unix system!")


## do argparsing, set global variables
arr = [int(x) for x in sys.argv[1:]]
mval = max(arr)
chwidth = 80 // len(arr)
chheight = 51 // mval

## fn to print the current permutation to screen
def printarr(arr, counter=None, chwidth=1, chheight=1):
    print("\033[F\033[K" * mval * chheight, end='')
    if counter:
        print("\033[F\033[K", end='')
        print(f"Step: {counter}")

    for x in range(mval, 0, -1):
        for _ in range(chheight):
            print(' '.join(['#'*chwidth if arr[i] > x else ' '*chwidth for i in range(len(arr))]))

## bogo sort, implemented faster than it ran
counter = 0
while sorted(arr) != arr:
    counter += 1
    random.shuffle(arr)
    time.sleep(0.2)
    printarr(arr, counter=counter, chwidth=chwidth, chheight=chheight)
    #print("\033[F\033[K", arr)

print(f"Done after {counter} steps!")
printarr(arr, chwidth=chwidth, chheight=chheight)
