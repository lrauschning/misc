#!/bin/env python3

def to_roman(x):
    if x <=3:
        return x*'I'
    elif x == 4 or x == 9:
        return 'I' + to_roman(x+1)
    elif x < 9:
        return 'V' + to_roman(x-5)
    else:
        return 'X' + to_roman(x-10)


if __name__ == '__main__':
    import sys
    print(to_roman(int(sys.argv[1])))

