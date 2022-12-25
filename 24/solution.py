import bisect
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

DIRS = {
    "<": (-1, 0),
    ">": (1, 0),
    "v": (0, 1),
    "^": (0, -1)
}

SIGNS = {
    (-1, 0): "<",
    (1, 0): ">",
    (0, 1): "v",
    (0, -1): "^"
}

# Part 1 solution : 
def part_1():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = np.array(read_lines_sep(filename, sep="", f=str))

    blizzards = set(((x, y), DIRS[elem]) for y, row in enumerate(data) for x, elem in enumerate(row) if elem in DIRS.keys())

    H, W = len(data), len(data[0])
    start = (1, 0)
    end = (W - 2, H - 1)

    B = [set(b for b, dir in blizzards.copy())]
    for _ in range(1000):
        blizzards, to_add = move_blizzards(blizzards, 1, H, W)
        B.append(to_add)
    
    visisted = set()
    p = heuristics(manhatten(*start, *end), 0)
    q = deque([(start, 0, None, p)])
    while q:
        current, steps, prev, pri = q.popleft()
            
        x, y = current

        if current == end:
            return steps

        current_blizz = B[steps]
        if current in current_blizz or (current, steps) in visisted:
            continue
        visisted.add((current, steps))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = x + dx
            new_y = y + dy
            if (new_x, new_y) == end:
                return steps + 1
            if new_x < 1 or new_x > W -2:
                continue
            if new_y < 1 or new_y > H -2 and (new_x, new_y) != end:
                continue
            if (new_x, new_y) in B[steps + 1]:
                continue
            p = heuristics(manhatten(new_x, new_y, *end), steps +1)
            bisect.insort(q, ((new_x, new_y), steps + 1, current, p), key=lambda x: x[3])

        p = heuristics(manhatten(x, y, *end), steps +1)
        bisect.insort(q, ((x, y), steps + 1, current, p), key=lambda x: x[3])


    return blizzards

def manhatten(x1, x2, y1, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def heuristics(distance, steps):
    return (distance) + steps

# Moves blizzards n steps
def move_blizzards(blizzards, n, H, W):
    for _ in range(n):
        new_blizzards = set()
        to_add = set()
        for (x, y), (dx, dy) in blizzards:
            new_x = x + dx
            new_y = y + dy
            if new_x < 1:
                new_x = W - 2
            if new_x > W - 2:
                new_x = 1
            if new_y < 1:
                new_y = H - 2
            if new_y > H - 2:
                new_y = 1
            new_blizzards.add(((new_x, new_y), (dx, dy)))
            to_add.add((new_x, new_y))
    return new_blizzards, to_add
        
        

# Part 2 solution : 
def part_2():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = np.array(read_lines_sep(filename, sep="", f=str))

    blizzards = set(((x, y), DIRS[elem]) for y, row in enumerate(data) for x, elem in enumerate(row) if elem in DIRS.keys())
    H, W = len(data), len(data[0])
    start = (1, 0)
    end = (W - 2, H - 1)

    B = [set(b for b, dir in blizzards.copy())]
    for _ in range(1000):
        blizzards, to_add = move_blizzards(blizzards, 1, H, W)
        B.append(to_add)
    
    tot_steps = 0
    for i in range(3):
        visisted = set()
        if i == 0:
            target = end
            p = heuristics(manhatten(*start, *target), 0)
            q = deque([(start, tot_steps, None, p)])
        elif i == 1:
            target = start
            p = heuristics(manhatten(*end, *target), 0)
            q = deque([(end, tot_steps, None, p)])
        elif i == 2:
            target = end
            p = heuristics(manhatten(*start, *target), 0)
            q = deque([(start, tot_steps, None, p)])

        while q:
            current, steps, prev, pri = q.popleft()
                
            x, y = current

            if current == target:
                tot_steps = steps
                print("STEPS:", steps)
                if i == 2:
                    return tot_steps
                time.sleep(1)
                break

            current_blizz = B[steps]
            if current in current_blizz or (current, steps) in visisted:
                continue
            visisted.add((current, steps))

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x = x + dx
                new_y = y + dy
                if new_x < 0 or new_x > W -1:
                    continue
                if new_y < 0 or new_y > H -1 and (new_x, new_y) != target:
                    continue
                if data[new_y, new_x] == "#":
                    continue
                if (new_x, new_y) in B[steps + 1]:
                    continue
                p = heuristics(manhatten(new_x, new_y, *target), steps +1)
                bisect.insort(q, ((new_x, new_y), steps + 1, current, p), key=lambda x: x[3])

            p = heuristics(manhatten(x, y, *target), steps +1)
            bisect.insort(q, ((x, y), steps + 1, current, p), key=lambda x: x[3])


    print("RETURNING")
    return tot_steps, "HAX"


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
