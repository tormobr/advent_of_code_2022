from collections import deque
import numpy as np

import sys
sys.path.insert(0,'..')
from advent_lib import *

DIRS = {
    "<": (-1, 0),
    ">": (1, 0),
    "v": (0, 1),
    "^": (0, -1)
}

# Part 1 solution : 
def part_1():
    return solve()

# Part 2 solution : 
def part_2():
    return solve(rounds=3)

def solve(rounds=1):
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"

    # Parse input data and create set of blizzards, and their directions
    data = np.array(read_lines_sep(filename, sep="", f=str))
    blizzards = set(((x, y), DIRS[elem]) for y, row in enumerate(data) for x, elem in enumerate(row) if elem in DIRS.keys())

    # Get width, height, start, end etc. from map
    H, W = len(data), len(data[0])
    start, end = (1, 0), (W - 2, H - 1)

    # Simulate blizzards a fair amount into the future and store it in list
    B = get_n_blizzards(blizzards, H, W, 1000)
    
    # Perform pathfind back and forth between start <-> end * "rounds" number of times
    tot_steps = 0
    for i in range(rounds):
        visisted = set()
        s = start
        target = end

        # flip start and end if current iteration dictates it
        if i % 2 != 0:
            target = start
            s = end

        q = deque([(s, tot_steps)])
        while q:
            current, steps = q.popleft()
            x, y = current

            # if current is target we have arrived at destination
            if current == target:
                tot_steps = steps
                break

            # if the current position is occupied by blizzard or has been visisted
            # at same number of steps before
            if (current, steps) in visisted or current in B[steps]:
                continue
            visisted.add((current, steps))

            # Add the neighbors to the que (if they are inside the map)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if not out_of_bounds(new_x, new_y, data, H, W):
                    q.append(((new_x, new_y), steps + 1))

            # Add the current position to the queue
            # as standing still is a valid option
            q.append((current, steps + 1))

    return tot_steps

# Checks if current x,y is outside map
def out_of_bounds(x, y, data, H, W):
    return ((x < 0 or x >= W)
        or (y < 0 or y >= H)
        or (data[y, x] == "#"))

# Moves blizzards n steps and returns array with state over time
def get_n_blizzards(blizzards, H, W, n):
    B = [set(b for b, dir in blizzards)]
    for _ in range(n):
        new_blizzards, blizzards_xy = set(), set()
        for (x, y), (dx, dy) in blizzards:
            new_x, new_y = x + dx, y + dy
            if new_x < 1:
                new_x = W - 2
            if new_x > W - 2:
                new_x = 1
            if new_y < 1:
                new_y = H - 2
            if new_y > H - 2:
                new_y = 1

            new_blizzards.add(((new_x, new_y), (dx, dy)))
            blizzards_xy.add((new_x, new_y))
        blizzards = new_blizzards
        B.append(blizzards_xy)

    return B
        
        
if __name__ == "__main__":
    s = time.time()
    p1 = part_1()
    e = time.time()
    t1 = e - s

    s = time.time()
    p2 = part_2()
    e = time.time()
    t2 = e - s

    pretty_print(p1, p2, t1, t2)
