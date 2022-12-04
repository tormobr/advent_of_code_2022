import sys
sys.path.insert(0,'..')
from advent_lib import *

# Identify if sections are completely overlapping
def completely_overlapping(x1, x2, y1, y2):
    return (x1 >= y1 and x2 <= y2 or
            y1 >= x1 and y2 <= x2)


# Identify if sections are partially overlapping
def partially_overlapping(x1, x2, y1, y2):
    return x1 <= y2 and x2 >= y1

# Converts string of kind "11-31" => (11, 31)
def get_pair(pair_str):
    return tuple((int(pair_str.split("-")[0]), int(pair_str.split("-")[1])))

# Part 1 solution : 
def part_1():
    return solve(completely_overlapping)

# Part 2 solution : 
def part_2():
    return solve(partially_overlapping)

# Generic method to solve problem with overlapping evaluator as input
def solve(evaluator):
    data = [(get_pair(pair) for pair in line.split(",")) for line in open("input.txt", "r")]

    return sum(1 for x, y in data if evaluator(*x, *y))


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
