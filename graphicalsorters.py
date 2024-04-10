#!/bin/python

import sys
import argparse
import random
import time
import os


## set global variables
DELAY = 2
WIDTH = 80
HEIGHT = 51

## fn to print the current permutation to screen
def printarr(arr, counter=None, highlight=None):
    mval = max(arr) + (0 if highlight is None else 1) # add a row for the arrow
    chwidth = WIDTH // len(arr)
    chheight = HEIGHT // mval

    # clear the cli
    print("\033[F\033[K" * mval * chheight, end='')

    if counter: # draw a counter in addition to array
        print("\033[F\033[K", end='')
        print(f"Step: {counter}")

    if highlight is not None: # highlight a position in the array by drawing an arrow
        arrowheadstart = chheight//3
        arrowheadslope = chwidth/(chheight - arrowheadstart)
        arrowheadwidth = chwidth - chwidth//3
        arrowheadoffset = chwidth - arrowheadwidth
        for j in range(chheight):
            i = j - arrowheadstart
            print(' '*chwidth*highlight, end='') # skip until highlight
            
            # draw the arrow
            if i < 0:
                print(' '*(arrowheadoffset + arrowheadwidth//2) + '#')# + ' '*(chwidth//2-1), end='')
            else:
                loc = int(i*arrowheadslope)
                print(' '*(arrowheadoffset+loc) + '#'*2*(arrowheadwidth//2-loc))

                #print(' '*(loc) + '\\' + ' '*(chwidth//2 - 1 - (loc)) + '|' + ' '*(chwidth//2 - 1 -loc) + '/' )

            # maybe also print spaces to match line width?
            #print(' '*chwidth*(len(arr) - highlight - 1))


    for x in range(mval, 0, -1):
        for _ in range(chheight):
            print(' '.join(['#'*chwidth if arr[i] > x else ' '*chwidth for i in range(len(arr))]))

def swap(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp

def bogosort(arr):
    counter = 0
    while sorted(arr) != arr:
        counter += 1
        random.shuffle(arr)
        time.sleep(DELAY)
        printarr(arr, counter=counter)
    return counter, arr


def gnomesort(arr):
    counter = 0
    ind = 0
    while ind < len(arr)-1:
        counter += 1
        printarr(arr, highlight=ind)
        time.sleep(DELAY)
        print(ind, arr)
        if arr[ind] > arr[ind+1]:
            swap(arr, ind, ind+1)
            ind = max(ind - 1, 0)
        else:
            ind += 1
    return counter, arr

def insertionsort(arr):
    counter = 0
    return counter, arr


if __name__ == '__main__':
    # quit if not on a unix system, there be terminal emulator dragons!
    if os.name == 'nt':
        raise OSError("It's not a unix system!")

    parser = argparse.ArgumentParser("A small script animating some common sorting algorithms on a CLI interface.")
    parser.add_argument("--height", type=int, default=51, help="Height of the animation in lines. Defaults to 51")
    parser.add_argument("-w", "--width", type=int, default=80, help="Width of the animation in lines. Defaults to 51")
    parser.add_argument('arr', nargs='*', type=int, help='List of Integers to sort')
    algos = parser.add_mutually_exclusive_group(required=True)
    algos.add_argument("--bogo", action='store_const', const=bogosort, dest='call', help="Use the bogosort algorithm.")
    algos.add_argument("--gnome", action='store_const', const=gnomesort, dest='call', help="Use the gnomesort algorithm.")
    algos.add_argument("--insertion", action='store_const', const=insertionsort, dest='call', help="Use the insertion sort algorithm.")

    args = parser.parse_args()

    # pass display options to global variables, less clean but less work
    HEIGHT = args.height
    WIDTH = args.width

    # do the sorting call
    counter, arr = args.call(args.arr)

    print(f"Done after {counter} steps!")
    printarr(arr)
