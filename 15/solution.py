import math
import numba
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
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines(filename, f=str)
    data = [tuple(ints(line)) for line in data]

    row = 2000000
    # row = 10
    not_valid = set()

    for sensor_x, sensor_y, beacon_x, beacon_y in data:
        distance_to_beacon = manhatten(beacon_x, sensor_x, beacon_y, sensor_y)
        distance_to_row = abs(row - sensor_y)
        spare_distance = distance_to_beacon - distance_to_row

        x_range = set(range(sensor_x - spare_distance, sensor_x + spare_distance))
        not_valid |= x_range

    return len(not_valid)

# Part 2 solution : 
def part_2():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines(filename, f=str)
    data = [tuple(ints(line)) for line in data]

    row = 2000000
    row = 10
    S = {}

    for sensor_x, sensor_y, beacon_x, beacon_y in data:
        S[(sensor_x, sensor_y)] = manhatten(beacon_x, sensor_x, beacon_y, sensor_y)

    return get_boarder_items(S)

def get_boarder_items(S):
    limit = 4000000
    limit = 20
    ret = set()
    for (sensor_x, sensor_y), distance in S.items():
        print(len(S), sensor_x)
        left_x, left_y = sensor_x - distance, sensor_y
        right_x, right_y = sensor_x + distance+1, sensor_y

        top_left = [(left_x + k, left_y - k) for k in range(distance+1)]
        bottom_left = [(left_x + k, left_y + k) for k in range(distance+1)]

        top_right = [(right_x - k, right_y - k) for k in range(distance+1)]
        bottom_right = [(right_x - k, right_y + k) for k in range(distance+1)]

        all = top_right + top_right + bottom_right + bottom_left

        for x, y in all:
            if is_valid(S, x, y) and x > 0 and x < limit and y > 0 and y < limit:
                ret.add((x, y))
                return x, y, (x * 4000000) + y

    return ret


def is_valid(S, x, y):
    for (sensor_x, sensor_y), distance in S.items():
        if manhatten(x, sensor_x, y, sensor_y) <= distance:
            return False
    return True

def manhatten(x1, x2, y1, y2):
    return abs(x2 - x1) + abs(y2 - y1)


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
