import re

import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    return DFS("root", parse_data())[0]

# Part 2 solution : 
def part_2():
    monkeys = parse_data()

    monkeys["root"] = monkeys["root"].replace("+", "==")
    return find_my_value(monkeys)

def parse_data():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = [line.strip().split(": ") for line in open(filename, "r")]

    return {splitted[0]: splitted[1] for splitted in data}

def find_my_value(monkeys):
   return ret if (ret := binomial(monkeys)) != None else binomial(monkeys, right_constant=False)

def binomial(monkeys, right_constant=True):
    # Create resonable amount of search space for our secrete number
    min_t, max_t = -int(10e20), int(10e20)
    t = max_t // 2

    while t < max_t and t > min_t:
        monkeys["humn"] = str(t)
        res, is_bigger = DFS("root", monkeys)
        if res == "1":
            return t

        if right_constant:
            min_t = t if is_bigger else min_t
            max_t = t if not is_bigger else max_t
        else:
            min_t = t if not is_bigger else min_t
            max_t = t if is_bigger else max_t
        t = (max_t + min_t) // 2 

    return None

def DFS(current, monkeys):
    if re.match("^-?\d+$", current):
        return current, None

    value = monkeys[current]
    if re.match("^-?\d+$", value):
        return int(value), None

    left, operator, right = value.split()
    calculated_left, calculated_right = DFS(left, monkeys)[0], DFS(right, monkeys)[0]

    result_evaluation = str(int(eval(f"{calculated_left} {operator} {calculated_right}")))
    result_evaluation_is_bigger = eval(f"{calculated_left} > {calculated_right}")

    return result_evaluation, result_evaluation_is_bigger
    
if __name__ == "__main__":
    pretty_print(part_1(), part_2())
