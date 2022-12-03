import sys
sys.path.insert(0,'..')
from advent_lib import *

a_ascii_value = 97
A_ascii_value = 65
def get_score(s):
    return ord(s) - A_ascii_value + 27 if s.isupper() else ord(s) - a_ascii_value + 1

# Part 1 solution : 
def part_1():
    sacks = [(set(line[:len(line)//2]), set(line[len(line)//2:])) for line in read_lines("input.txt", f=str)]

    return sum(sum(get_score(item) for item in (a & b)) for a, b in sacks)

# Part 2 solution : 
def part_2(n=3):
    sacks = [set(sack) for sack in read_lines("input.txt", f=str)]

    groups = [sacks[i:i+n] for i in range(0, len(sacks) - n+1, n)]

    return sum(get_score(list(set.intersection(*group))[0]) for group in groups)


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
