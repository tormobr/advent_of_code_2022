import math
from collections import deque, defaultdict
from functools import reduce
from operator import mul
import itertools
import numpy as np
import re

import sys
sys.path.insert(0,'..')
from advent_lib import *



def move(n, fromm, to, stacks):
    for _ in range(n):
        value = stacks[fromm].pop()
        stacks[to].append(value)

    return stacks

def move2(n, fromm, to, stacks):
    popped = stacks[fromm][-n: ]
    stacks[fromm] = stacks[fromm][:-n]
    stacks[to] += popped

    return stacks

    for _ in range(n):
        if len(stacks[fromm]) == 0:
            continue
        value = stacks[fromm].pop()
        stacks[to].append(value)

    return stacks


# Part 1 solution : 
def part_1():

    crates, moves = open("input.txt", "r").read().split("\n\n")
    chars = [[c for c in line] for line in crates.split("\n")]

    stacks = []
    current_stack = 0
    for col in range(1, len(chars[0]), 4):
        stacks.append([])
        for row in range(len(chars)-1):
            if chars[row][col] != " ":
                stacks[current_stack].append(chars[row][col])
        current_stack += 1

    moves = [tuple(ints(line)) for line in moves.split("\n")][:-1]

    stacks = [stack[::-1] for stack in stacks]
    for n, fromm, to in moves:
        stacks = move(n, fromm-1, to-1, stacks)

    lasts = "".join([stack[-1] for stack in stacks])
    return lasts

# Part 2 solution : 
def part_2():
    crates, moves = open("input.txt", "r").read().split("\n\n")
    chars = [[c for c in line] for line in crates.split("\n")]

    stacks = []
    current_stack = 0
    for col in range(1, len(chars[0]), 4):
        stacks.append([])
        for row in range(len(chars)-1):
            if chars[row][col] != " ":
                stacks[current_stack].append(chars[row][col])
        current_stack += 1

    moves = [tuple(ints(line)) for line in moves.split("\n")][:-1]

    stacks = [stack[::-1] for stack in stacks]
    for n, fromm, to in moves:
        stacks = move2(n, fromm-1, to-1, stacks)

    lasts = "".join([stack[-1] for stack in stacks])
    return lasts


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
