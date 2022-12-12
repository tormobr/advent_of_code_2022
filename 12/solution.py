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
    terrain = np.array([[c for c in line.strip()] for line in open("input.txt", "r")])

    start = list(zip(*np.where(terrain == "S")))[0]
    end = list(zip(*np.where(terrain == "E")))[0]
    terrain[start] = "a"
    terrain[end] = "z"
    return bfs(start, end, terrain)


# Part 2 solution : 
def part_2():
    terrain = np.array([[c for c in line.strip()] for line in open("input.txt", "r")])

    start = list(zip(*np.where(terrain == "S")))[0]
    end = list(zip(*np.where(terrain == "E")))[0]

    starts = list(zip(*np.where(terrain == "a"))) + [start]
    terrain[start] = "a"
    terrain[end] = "z"

    results = [bfs(ss, end, terrain) for ss in starts]
    return min(r for r in results if r != None)

def bfs(start, end, terrain):
    q = [(start, 0)]
    visited = set()

    while q:
        current, steps = q.pop(0)
        if current in visited:
            continue

        visited.add((current))

        if current == end:
            return steps

        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_y = current[0] + dy
            new_x = current[1] + dx
            if new_y >= terrain.shape[0] or new_y < 0 or new_x >= terrain.shape[1] or new_x < 0:
                continue

            if (ord(terrain[new_y, new_x]) - ord(terrain[current]) < 2):
                q.append(((new_y, new_x), steps + 1))

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
