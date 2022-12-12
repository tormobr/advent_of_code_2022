import math
from collections import deque, defaultdict
from functools import reduce
from operator import mul, add
import itertools
import numpy as np
import re

import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    monkey_dict = generate_monkey_dict()
    return do_monkey_business(monkey_dict, lambda x, y: x // 3)

# Part 2 solution : 
def part_2():
    monkey_dict = generate_monkey_dict()
    return do_monkey_business(monkey_dict, lambda x, y: x % y, rounds=10000)

def generate_monkey_dict():
    monkeys = open("input.txt", "r").read().split("\n\n")

    monkey_dict = defaultdict(lambda: {})
    for monkey in monkeys[:-1]:
        lines = [line.strip() for line in monkey.split("\n")]

        monkey_key = ints(lines[0])[0]
        properties = lines[1:]
        assert(len(properties) == 5)

        starting_items, operation, test, if_true, if_false = properties

        monkey_dict[monkey_key]["items"] = ints(starting_items)
        monkey_dict[monkey_key]["operation"] = get_operation(operation)
        monkey_dict[monkey_key]["test"] = ints(test)[0]
        monkey_dict[monkey_key]["iftrue"] = ints(if_true)[0]
        monkey_dict[monkey_key]["iffalse"] = ints(if_false)[0]

    return monkey_dict

def do_monkey_business(monkey_dict, modify, rounds=20):
    n_monkyes = max(key for key in monkey_dict.keys()) + 1
    current_round = 0
    inspections = defaultdict(int)

    lcm = np.lcm.reduce([m["test"] for m in monkey_dict.values()])

    while current_round < rounds:
        for m in range(n_monkyes):
            current_monkey = monkey_dict[m]
            for item in current_monkey["items"]:

                inspections[m] += 1
                left, right, operator = current_monkey["operation"]
                if left == "old":
                    left = item
                if right == "old":
                    right = item

                item = operator(int(left), int(right))
                item = modify(item, lcm)

                if item % current_monkey["test"] == 0:
                    monkey_dict[current_monkey["iftrue"]]["items"].append(item)
                else:
                    monkey_dict[current_monkey["iffalse"]]["items"].append(item)

            current_monkey["items"] = []

        current_round += 1

    return reduce(mul, sorted(inspections.values())[::-1][:2])

def get_operation(s):
    left = s.split()[3]
    right = s.split()[5]
    if "+" in s:
        operator = add
    if "*" in s:
        operator = mul
    return (left, right, operator)

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
