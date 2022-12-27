from collections import deque, defaultdict
from functools import reduce
from operator import mul
import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines(filename, f=str)

    blueprints = parse_data(data)
    results = solve(blueprints, mins=24)
    return sum(r * (i+1) for i, r in enumerate(results))

# Part 2 solution : 
def part_2():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines(filename, f=str)[:3]

    blueprints = parse_data(data)
    results = solve(blueprints, mins=32)
    return reduce(mul, results)


# Iterates all the blueprints and gather the best result from each of them
def solve(blueprints, mins=24):
    # State is (current holdings, minutes)
    res = []
    for id, blueprint in blueprints.items():
        costs, maxes = blueprint["costs"], blueprint["maxes"]
        res.append(get_best(costs, maxes, mins))
    return res

# DFS to find the best option for a single blueprint
def get_best(costs, maxes, mins):
    b, h = defaultdict(int), defaultdict(int)
    b["ore"] = 1

    best = 0 
    visisted = set()
    q = deque([(b, h, mins, h, "")])
    while q:
        bots, holdings, minutes, previous_holdings, bought_bot = q.popleft()

        # Add current state to set of states if it hasn't been visited before
        state = get_state(bots, holdings, minutes, maxes)
        if state in visisted:
            continue
        visisted.add(state)


        # If we are out of time check if result is better than current best
        if minutes < 1:
            best = max(best, holdings["geode"])
            continue

        # Update holdings
        last_holdings = holdings.copy()
        for k, v in bots.items():
            holdings[k] += v

        # If it is impossible to attain more geodes even with best best case
        # while continuing on this branch
        if best_case_geodes(holdings, bots, minutes) < best:
            continue

        q.appendleft((bots.copy(), holdings.copy(), minutes - 1, last_holdings, ""))

        for to_get, cost_dict in costs.items():

            # Pruning branches if we already have enough bots of this kind
            if bots[to_get] >= maxes[to_get] or bots[to_get] * minutes + holdings[to_get] >= maxes[to_get] * minutes:
                continue

            # Pruning branches if we could afford it in last step but didn't buy it
            if can_afford(previous_holdings, cost_dict) and bought_bot == "":
                continue

            if can_afford(last_holdings, cost_dict):
                next_holdings = holdings.copy()
                next_bots = bots.copy()
                next_bots[to_get] += 1
                for item_needed, amount in cost_dict.items():
                    next_holdings[item_needed] -= amount
                q.appendleft((next_bots, next_holdings, minutes - 1, last_holdings, to_get))

    return best

# calculate the best possible number of geodes based on current robots and minutes
def best_case_geodes(bots, holdings, minutes):
    geode_bots = bots["geode"]
    geode_holdings = holdings["geode"]
    return geode_holdings + (geode_bots * minutes) + (minutes * (minutes/2) + minutes / 2)

# check if we can afford a robot with given holdings
def can_afford(holdings, cost_dict):
    for item_needed, amount in cost_dict.items():
        if holdings[item_needed] < amount:
            return False
    return True

# Creates a state for the current branch
def get_state(bots, holdings, minutes, maxes):
    b = tuple((bots["ore"], bots["clay"], bots["obsidian"], bots["geode"]))

    # Normalize state of holdings to get more cache hits
    h = tuple((holdings["ore"] % maxes["ore"], holdings["clay"] % maxes["clay"], holdings["obsidian"] % maxes["obsidian"], holdings["geode"] % maxes["geode"]))
    return (b, h, minutes)

# Reads input lines and creates dictionary with blueprint information
def parse_data(data):
    blueprints = defaultdict(lambda: defaultdict(dict))
    for line in data:
        (id,
         cost_ore_ore,
         cost_clay_ore,
         cost_obsidian_ore,
         cost_obsidian_clay,
         cost_geode_ore,
         cost_geode_obsidian) = ints(line)
        blueprints[id]["costs"]["ore"] = {"ore": cost_ore_ore}
        blueprints[id]["costs"]["clay"] = {"ore": cost_clay_ore}
        blueprints[id]["costs"]["obsidian"] = {"ore": cost_obsidian_ore, "clay": cost_obsidian_clay}
        blueprints[id]["costs"]["geode"] = {"ore": cost_geode_ore, "obsidian": cost_geode_obsidian}

        blueprints[id]["maxes"]["ore"] = max(cost_ore_ore, cost_obsidian_ore, cost_clay_ore, cost_geode_ore)
        blueprints[id]["maxes"]["clay"] = cost_obsidian_clay
        blueprints[id]["maxes"]["obsidian"] = cost_geode_obsidian
        blueprints[id]["maxes"]["geode"] = 10000

    return blueprints


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
