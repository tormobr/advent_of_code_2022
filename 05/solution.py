import numpy as np
import re

import sys
sys.path.insert(0,'..')
from advent_lib import *



def move_basic(n, origin, destination, stacks):
    for _ in range(n):
        stacks[destination].append(stacks[origin].pop())

def move_advanced(n, origin, destination, stacks):
    popped = stacks[origin][-n:]
    stacks[origin] = stacks[origin][:-n]
    stacks[destination] += popped

def solve(move_strategy):
    crates, moves = open("input.txt", "r").read().split("\n\n")

    crate_chars = [[c for c in line] for line in crates.split("\n")]
    crate_chars_rotated = np.rot90(crate_chars, axes=(1, 0))
    stacks = [[elem for elem in row[1:] if not re.match("\s+", elem)] for row in crate_chars_rotated if re.match("\d", row[0])]

    moves = [tuple(ints(line)) for line in moves.split("\n")][:-1]

    for n, origin, destination in moves:
        move_strategy(n, origin-1, destination-1, stacks)

    return "".join([stack[-1] for stack in stacks])

# Part 1 solution : 
def part_1():
    return solve(move_basic)

# Part 2 solution : 
def part_2():
    return solve(move_advanced)

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
