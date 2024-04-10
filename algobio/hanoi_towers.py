#!/usr/bin/python
from datetime import datetime


def _hanoi_recursive(i, start, dest, aux):
    if i <= 1:
        lst_recursive.append(f"{start} --> {dest}")
        return
    _hanoi_recursive(i - 1, start, aux, dest)
    lst_recursive.append(f"{start} --> {dest}")
    _hanoi_recursive(i - 1, aux, dest, start)


class Stack:
    def __init__(self, storage):
        self.storage = storage
        self.length = -1
        self.array = [0 for i in range(storage)]

    def is_full(self):
        return self.length == self.storage - 1

    def is_empty(self):
        return self.length == -1


# put_disk a disk onto a stack
def put_disk(stack, item):
    if stack.is_full():
        return
    stack.array[stack.length + 1] = item
    stack.length += 1


# get the topmost element of a stack
def get_disk(stack):
    if stack.is_empty():
        return float("-inf")
    stack.length -= 1
    return stack.array[stack.length + 1]


def move_disks_between_pins(pin1, pin2, pin1_name, pin2_name):
    pin1_top_disk = get_disk(pin1)
    pin2_top_disk = get_disk(pin2)

    # Pin 1 is empty
    if pin1_top_disk == float("-inf"):
        put_disk(pin1, pin2_top_disk)
        move_disk(pin2_name, pin1_name)

    # Pin 2 is empty
    elif pin2_top_disk == float("-inf"):
        put_disk(pin2, pin1_top_disk)
        move_disk(pin1_name, pin2_name)

    # Pin 1 disk > Pin 2 disk
    elif pin1_top_disk > pin2_top_disk:
        put_disk(pin1, pin1_top_disk)
        put_disk(pin1, pin2_top_disk)
        move_disk(pin2_name, pin1_name)

    # Pin 2 disk > Pin 1 disk
    else:
        put_disk(pin2, pin2_top_disk)
        put_disk(pin2, pin1_top_disk)
        move_disk(pin1_name, pin2_name)


# Method to move a disk from start to destination
def move_disk(start, dest):
    lst_iterative.append(f"{start} --> {dest}")


def _hanoi_iterative(n, start, aux, dest):
    # Store names of the stacks
    s = start
    d = dest
    a = aux

    start_pin = Stack(n)
    aux_pin = Stack(n)
    dest_pin = Stack(n)

    if n % 2 == 0:
        a, d = d, a

    calculated_moves = (2 ** n) - 1

    for i in range(n, 0, -1):
        put_disk(start_pin, i)

    for i in range(1, calculated_moves + 1, 1):
        if i % 3 == 1:
            move_disks_between_pins(start_pin, dest_pin, s, d)
        elif i % 3 == 2:
            move_disks_between_pins(start_pin, aux_pin, s, a)
        elif i % 3 == 0:
            move_disks_between_pins(aux_pin, dest_pin, a, d)


def hanoi_recursive(n, start_pin, dest_pin):
    aux_pin = [i for i in ["A", "B", "C"] if i not in (start_pin, dest_pin)][0]
    _hanoi_recursive(n, start_pin, dest_pin, aux_pin)


def hanoi_iterative(n, start_pin, dest_pin):
    aux_pin = [i for i in ["A", "B", "C"] if i not in (start_pin, dest_pin)][0]
    _hanoi_iterative(n, start_pin, aux_pin, dest_pin)


# Store moves of both algorithms
lst_recursive = []
lst_iterative = []
"""
n = 6

hanoi_iterative(n, "A", "C")
hanoi_recursive(n, "A", "C")

print("Rekursiv:", lst_recursive)
print("Iterativ:", lst_iterative)
print(lst_iterative == lst_recursive)

"""
# Benchmarking
for n in [5, 10, 15, 20, 25, 30]:
    start = datetime.now()
    hanoi_iterative(n, "A", "C")
    end = datetime.now()
    print(f"iterative {n} {end - start}")
    start = datetime.now()
    hanoi_recursive(n, "A", "C")
    end = datetime.now()
    print(f"recursive {n} {end - start}")

