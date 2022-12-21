from collections import deque

import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    return solve()

# Part 2 solution : 
def part_2(is_part_2=False):
    return solve(is_part_2=True)

# Part 2 solution : 
def solve(is_part_2=False):
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = set(tuple(line) for line in read_lines_sep(filename, sep=",", f=int))

    max_x = max(data, key=lambda x: x[0])[0] + 5
    max_y = max(data, key=lambda x: x[1])[1] + 5
    max_z = max(data, key=lambda x: x[2])[2] + 5

    min_x = min(data, key=lambda x: x[0])[0] - 5
    min_y = min(data, key=lambda x: x[1])[1] - 5
    min_z = min(data, key=lambda x: x[2])[2] - 5

    q = deque([(min_x, min_y, min_z)])
    surfaces = 0
    visisted = set()
    while q:
        x, y, z = item = q.popleft()

        if item in visisted or (is_part_2 and item in data):
            continue

        visisted.add(item)

        # Hack to penetrate barrier if we are solving for part 1
        if is_part_2 or (item not in data and not is_part_2):
            surfaces += 1 if (x+1, y, z) in data else 0
            surfaces += 1 if (x, y+1, z) in data else 0
            surfaces += 1 if (x, y, z+1) in data else 0
            surfaces += 1 if (x-1, y, z) in data else 0
            surfaces += 1 if (x, y-1, z) in data else 0
            surfaces += 1 if (x, y, z-1) in data else 0

        for dx, dy, dz in SPIN_DIRS_3D:
            new_x, new_y, new_z = x+dx, y+dy, z+dz
            new_item = (new_x, new_y, new_z)
            if not out_of_bounds(new_item, max_x, max_y, max_z, min_x, min_y, min_z):
                q.append(new_item)


    return surfaces

def out_of_bounds(item, max_x, max_y, max_z, min_x, min_y, min_z):
    x, y, z = item
    if x < min_x or x >= max_x:
        return True
    if y < min_y or y >= max_y:
        return True
    if z < min_z or z >= max_z:
        return True

    return False


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
