import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    return solve(4)

# Part 2 solution : 
def part_2():
    return solve(14)

def solve(packet_length):
    chars = [c for c in open("input.txt", "r").read()]
    for i in range(packet_length, len(chars)):
        if len(set(chars[i - packet_length: i])) == packet_length:
            return i


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
