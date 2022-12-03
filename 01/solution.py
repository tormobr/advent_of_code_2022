import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    elves = [[int(item) for item in elf.split("\n") if item != ""] for elf in open("input.txt", "r").read().split("\n\n")]
    return max(sum(items) for items in elves)

# Part 2 solution : 
def part_2():
    elves = [[int(item) for item in elf.split("\n") if item != ""] for elf in open("input.txt", "r").read().split("\n\n")]
    return sum(sorted(sum(items) for items in elves)[-3:])


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
