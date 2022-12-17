from functools import cmp_to_key

import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    groups = [tuple(item.strip() for item in g.split("\n")) for g in open("input.txt", "r").read().split("\n\n")][:-1]

    group_results = [compare(eval(left), eval(right)) for left, right in groups]
    return sum(i + 1 for i, x in enumerate(group_results) if x == 1)

# Part 2 solution : 
def part_2():
    data = [eval(line.strip()) for line in open("input.txt", "r") if line != "\n"]
    data = data + [[[2]], [[6]]]

    data_sorted = sorted(data, key=cmp_to_key(compare), reverse=True)

    return (data_sorted.index([[2]]) + 1) * (data_sorted.index([[6]]) + 1)

def compare(left, right):
    if type(left) == list and type(right) == list:
        for l, r in zip(left, right):
            if (c := compare(l, r)) != 0:
                return c
        return calculate_return(len(left), len(right))

    if type(left) == list and type(right) == int:
        return compare(left, [right])

    if type(left) == int and type(right) == list:
        return compare([left], right)

    return calculate_return(left, right)

def calculate_return(left, right):
    if left < right:
        return 1
    elif left == right: 
        return 0
    return -1

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
