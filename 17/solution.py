
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

# List over possible rocks
ROCKS = [
    [["#", "#", "#", "#"]],

    [[".", "#", "."],
     ["#", "#", "#"],
     [".", "#", "."]],

    [[".", ".", "#"],
     [".", ".", "#"],
     ["#", "#", "#"]],

    [["#"],
     ["#"],
     ["#"],
     ["#"]],

    [["#", "#"],
     ["#", "#"]]
]

# Height and width of "map"
W = 7
H = 10000000000000

# Part 1 solution : 
def part_1():
    return solve()

# Part 2 solution : 
def part_2():
    return solve(limit=1000000000000)

def solve(limit=2022):
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = [c for line in open(filename).read() for c in line.strip()]

    rock_index, input_index, rocks_placed = 0, 0, 0
    current_rock = ROCKS[rock_index]
    current_x, current_y = 2, H - 5

    # Add flor at bottom
    solid = set()
    for x in range(W):
        solid.add((x, H-1))

    tops = [H] * W  # List over top y coordinate for each column
    state_data = {}
    cycle_found = False
    states = set()
    cycle_addon = 0

    while rocks_placed < limit:
        dir = data[input_index]

        # Move the piece to side if possible
        if dir == ">" and can_move_right(current_rock, solid, current_x, current_y):
            current_x += 1
        elif dir == "<" and can_move_left(current_rock, solid, current_x, current_y):
            current_x -= 1

        # check if piece should be stopped
        stopped = False
        for y, row in enumerate(current_rock):
            for x, elem in enumerate(row):
                if elem == "#":
                    if (current_x + x, current_y + y+1) in solid:
                        stopped = True;

        if not stopped:
            current_y += 1
            input_index = (input_index + 1) % len(data)
            continue

        # If piece has stopped, update the set with solid rock coordinates
        for y, row in enumerate(current_rock):
            for x, elem in enumerate(row):
                if elem == "#":
                    # Keep track of current tops in each column to spot repetition
                    if current_y + y < tops[current_x + x]:
                        tops[current_x + x] = current_y - (current_y + y)
                    solid.add((current_x+x, current_y+y))

        # Add the "board" state to set to identify cycles later
        state = (tuple(tops.copy()), input_index % len(data), rock_index % len(ROCKS))
        if state in states and not cycle_found:
            cycle_found = True
            cycle_start = state_data[state]
            rocks_placed, cycle_addon = found_cycle(rocks_placed, get_height(solid), *cycle_start, limit)

        # add state to set of states and update state data dictonary
        states.add(state)
        state_data[state] = rocks_placed, get_height(solid)

        # Update rock index, number of rocks placed, coordinates, etc...
        input_index = (input_index + 1) % len(data)
        rock_index = (rock_index + 1) % len(ROCKS)
        current_rock = ROCKS[rock_index]
        rocks_placed += 1
        current_y = min(solid, key=lambda x: x[1])[1] - 3 - len(current_rock)
        current_x = 2


    # return (abs(min(solid, key=lambda x: x[1])[1] - H ) - 1)
    return (abs(min(solid, key=lambda x: x[1])[1] - H ) - 1) + cycle_addon

# If cycle if found this funciton calculates the height gained from repeating cycle n times
def found_cycle(tot_rocks_placed, tot_height, rocks_placed_before, height_before, limit):
    rocks_per_cycle = (tot_rocks_placed - rocks_placed_before)
    height_per_cycle = tot_height - height_before
    cycle_per_limit = (limit - rocks_placed_before) // rocks_per_cycle
    height_from_cycles = (cycle_per_limit - 1) * height_per_cycle # -1 to subtract the already counted first cycle

    new_rocks_placed = (rocks_per_cycle * cycle_per_limit) + rocks_placed_before
    return new_rocks_placed, height_from_cycles

# Gets the current top of map
def get_height(solid):
    return abs(min(solid, key=lambda x: x[1])[1] - H ) - 1

# Check of piece can be moved right. Please don't judge this horrible code
def can_move_right(current_rock, solid, current_x, current_y):
    for y in range(len(current_rock)):
        if current_rock == ROCKS[1]:
            if y == 0 or y == 2:
                if current_x + 2 >= W or (current_x + 2, current_y+y) in solid:
                    return False
            elif y == 1:
                if current_x + len(current_rock[0]) >= W or (current_x + len(current_rock[0]), current_y+y) in solid:
                    return False
        else:
            if current_x + len(current_rock[0]) >= W or (current_x + len(current_rock[0]), current_y+y) in solid:
                return False

    return True

# Check of piece can be moved left. Please don't judge this horrible code
def can_move_left(current_rock, solid, current_x, current_y):
    for y in range(len(current_rock)):
        if current_rock == ROCKS[1]:
            if y == 0 or y == 2:
                if current_x <= 0 or (current_x, current_y + y) in solid:
                    return False
            elif y == 1:
                if current_x <= 0 or (current_x - 1, current_y + y) in solid:
                    return False
        elif current_rock == ROCKS[2]:
            if y == 0 or y == 1:
                if current_x <= 0 or (current_x + 1, current_y + y) in solid:
                    return False
            elif y == 2:
                if current_x <= 0 or (current_x - 1, current_y + y) in solid:
                    return False
        else:
            if current_x <= 0 or (current_x - 1, current_y + y) in solid:
                return False
    return True

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
