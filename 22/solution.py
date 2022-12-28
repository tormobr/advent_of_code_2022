import constants
import re
import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    return solve(basic_wrapping)

def part_2():
    return solve(cube_wrapping)

def solve(wrapping_function):
    map, instructions = parse_data()
    tiles, blocked = create_tile_sets(map)

    current_tile = min([(x, y) for x, y in tiles if y == 0], key=lambda x: x[0])
    current_dir = (1, 0)

    for instruction in instructions:
        if re.match("(R|L)", instruction):
            current_dir = constants.TURNS[(current_dir, instruction)]
            continue

        for i in range(1, int(instruction) + 1):
            new_tile = current_tile[0] + current_dir[0], current_tile[1] + current_dir[1]
            if new_tile in blocked:
                break

            if new_tile not in tiles:
                new_tile, new_direction = wrapping_function(tiles, blocked, current_tile, current_dir)
                current_dir = new_direction
            current_tile = new_tile

    col, row, facing = current_tile[0] +1, current_tile[1] + 1, get_facing(current_dir)
    return (row * 1000) + (col * 4) + facing


def get_current_zone(current_tile):
    x, y = current_tile
    for k, (x_range, y_range) in constants.ZONES.items():
        if x in x_range and y in y_range:
            return k

def get_facing(direction):
    match direction:
        case (1, 0): return 0
        case (0, 1): return 1
        case (-1, 0): return 2
        case (0, -1): return 3

def get_normalized_position(position, zone):
    x, y = position
    x_range, y_range = constants.ZONES[zone]
    return (x - x_range[0], y - y_range[0])


def cube_wrapping(tiles, blocked, position, direction):
    current_zone = get_current_zone(position)
    new_zone, new_direction, flipping = constants.MOVEMENTS[current_zone][direction]

    norm_x, norm_y = get_normalized_position(position, current_zone)

    # Only y needs flipping
    if flipping == (0, 1):
        new_x = norm_x
        new_y = abs(49 - norm_y)

    # x and y flip places
    elif flipping == (1, 1):
        new_x = norm_y
        new_y = norm_x

    x_range, y_range = constants.ZONES[new_zone]
    new_tile = (x_range[0] + new_x, y_range[0] + new_y)

    return (position, direction) if new_tile in blocked else (new_tile, new_direction)

def basic_wrapping(tiles, blocked, position, direction):
    current_x, current_y = position
    dx, dy = direction
    if dx == 1:
        new_tile = min([(x, y) for x, y in tiles if y == current_y], key=lambda x: x[0])
    elif dx == -1:
        new_tile = max([(x, y) for x, y in tiles if y == current_y], key=lambda x: x[0])
    if dy == 1:
        new_tile = min([(x, y) for x, y in tiles if x == current_x], key=lambda x: x[1])
    elif dy == -1:
        new_tile = max([(x, y) for x, y in tiles if x == current_x], key=lambda x: x[1])

    return (position, direction) if new_tile in blocked else (new_tile, direction)
        
# Creates set of tiles which can be moved on, and blocked tiles
def create_tile_sets(map):
    tiles, blocked = set(), set()
    for y, row in enumerate(map):
        for x, elem in enumerate(row):
            if elem in [".", "#"]:
                tiles.add((x, y))
                if elem == "#":
                    blocked.add((x, y))

    return tiles, blocked

def parse_data():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = [line for line in open(filename, "r")]
    data = [[c for c in line][:-1] for line in data]
    map = data[:-2]
    instructions_array = data[-1]

    current, instructions = "", []
    for elem in instructions_array:
        if re.match("\d", elem):
            current += elem
        else:
            instructions.append(current)
            instructions.append(elem)
            current = ""

    instructions.append(current)

    return map, instructions

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
