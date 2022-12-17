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

# Part 1 solution : 
def part_1():
    rocks = build_map()
    return simulate_sand(rocks, lambda sand, max_y, sand_spawn: sand[1] > max_y)

# Part 2 solution : 
def part_2():

    rocks = build_map()

    # Add reasonable amount of floor
    floor = max(rocks, key=lambda x: x[1])[1] + 2
    for i in range(-1000, 1000):
        rocks.add((i, floor))

    return simulate_sand(rocks, lambda sand, max_y, sand_spawn: sand == sand_spawn)

def build_map():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = [[list(map(int, (elem.split(",")[0], elem.split(",")[1]))) for elem in line] for line in read_lines_sep(filename, sep=" -> ", f=str)]

    rocks = set()
    for line in data:
        prev_x, prev_y = line[0]
        for x, y in line:
            rocks.add((x, y))
            for current_y in range(min(prev_y, y), max(prev_y, y)):
                rocks.add((x, current_y))
            for current_x in range(min(prev_x, x), max(prev_x, x)):
                rocks.add((current_x, y))
            prev_x, prev_y = x, y

    return rocks

def simulate_sand(rocks, evaluate_completion):
    max_y = max(rocks, key=lambda x: x[1])[1]
    sand_spawn = (500, 0)
    sand = sand_spawn
    sands = set()
    while True:
        sand, did_move = move_sand(sand, rocks)
        if not did_move:
            rocks.add(sand)
            sands.add(sand)
        
        if evaluate_completion(sand, max_y, sand_spawn):
            return len(sands)

        if not did_move:
            sand = sand_spawn

def move_sand(sand, rocks):
    sand_x, sand_y = sand
    if (sand_x, sand_y +1) not in rocks:
        return (sand_x, sand_y +1), True
    elif (sand_x-1, sand_y +1) not in rocks:
        return (sand_x-1, sand_y +1), True
    elif (sand_x+1, sand_y +1) not in rocks:
        return (sand_x+1, sand_y +1), True
    return sand, False

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
