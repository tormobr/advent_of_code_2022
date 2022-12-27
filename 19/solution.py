import random
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

# Part 1 solution : 
def part_1():
    blueprints = parse_data()
    results = solve(blueprints, mins=24)
    return sum(r * i+1 for i, r in enumerate(results))

# Part 2 solution : 
def part_2():
    blueprints = parse_data(is_part_2=True)
    results = solve(blueprints, mins=32)
    return reduce(mul, results)

def parse_data(is_part_2=False):
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines(filename, f=str)
    blueprints = defaultdict(lambda: defaultdict(dict))
    if is_part_2:
        data = data[:3]
    for line in data:
        (id,
         cost_ore_ore,
         cost_clay_ore,
         cost_obsidian_ore,
         cost_obsidian_clay,
         cost_geode_ore,
         cost_geode_obsidian) = ints(line)
        blueprints[id]["ore"] = {"ore": cost_ore_ore}
        blueprints[id]["clay"] = {"ore": cost_clay_ore}
        blueprints[id]["obsidian"] = {"ore": cost_obsidian_ore, "clay": cost_obsidian_clay}
        blueprints[id]["geode"] = {"ore": cost_geode_ore, "obsidian": cost_geode_obsidian}

    return blueprints

def solve(blueprints, mins=24):

    # State is (current holdings, minutes)
    res = []
    res2 = []
    for id, costs in blueprints.items():
        maxes = defaultdict(int)
        for key in costs.keys():
            for values in costs.values():
                for k, v in values.items():
                    if k == key and v > maxes[key]:
                        maxes[key] = v
        maxes["geode"] = 10000

        b = defaultdict(int)
        h = defaultdict(int)
        b["ore"] += 1
        q = deque([(b, h, mins, h, "")])
        best = 0 
        best_bots = None
        visisted = set()
        first_geode = 0
        while q:
            current_bots, current_holdings, minutes, prev_prev_holdings, bought_bot = q.popleft()
            state = get_state(current_bots, current_holdings, minutes, maxes)
            if state in visisted:
                continue
            visisted.add(state)

            # print(f"\n{HEADER}-------------- MINUTE: {25 - minutes} -----------------{ENDC}")
            # print(f"{HEADER}Bots: {ENDC}\n{current_bots}")
            # print(f"{HEADER}holdings: {ENDC}\n{current_holdings}")
            # time.sleep(3)
            prev_holdings = current_holdings.copy()
            if minutes < 1:
                if current_holdings["geode"] > best:
                    best = current_holdings["geode"]
                    best_bots = current_bots
                    print(best, minutes, first_geode)
                continue

            # Update holdings
            for k, v in current_bots.items():
                current_holdings[k] += v

            if minutes < first_geode and current_holdings["geode"] == 0:
                continue

            if not all(x >= maxes[k] for k, x in current_holdings.items()):
                q.appendleft((current_bots.copy(), current_holdings.copy(), minutes - 1, prev_holdings, ""))

            for to_get, cost_dict in costs.items():
                if can_afford(prev_holdings, cost_dict):
                    afford_in_last_step = can_afford(prev_prev_holdings, cost_dict)
                    if (afford_in_last_step and bought_bot == ""):
                        continue

                    if current_bots[to_get] < maxes[to_get]:
                        new_holdings = current_holdings.copy()
                        new_bots = current_bots.copy()
                        new_bots[to_get] += 1
                        if new_bots["geode"] == 1 and to_get == "geode":
                            first_geode = minutes - 1
                        for item_needed, amount in cost_dict.items():
                            new_holdings[item_needed] -= amount
                        q.appendleft((new_bots, new_holdings, minutes - 1, prev_holdings, to_get))


        res.append(best)
        print(f"{OKGREEN}{best}{ENDC}")
    return res

def can_afford(holdings, cost_dict):
    for item_needed, amount in cost_dict.items():
        if holdings[item_needed] < amount:
            return False
    return True

def get_state(bots, holdings, minutes, maxes):
    b = tuple((bots["ore"], bots["clay"], bots["obsidian"], bots["geode"]))
    h = tuple((holdings["ore"] % maxes["ore"], holdings["clay"] % maxes["clay"], holdings["obsidian"] % maxes["obsidian"], holdings["geode"] % maxes["geode"]))
    return (b, h, minutes)


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
