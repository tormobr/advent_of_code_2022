import sys
sys.path.insert(0,'..')
from advent_lib import *

# the score for picking specific weapon
PICK_SCORE = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

# A dictionary containing rules over who wins given a selection
RULES = {
    ("A", "X"): 3,
    ("A", "Y"): 6,
    ("A", "Z"): 0,

    ("B", "X"): 0,
    ("B", "Y"): 3,
    ("B", "Z"): 6,

    ("C", "X"): 6,
    ("C", "Y"): 0,
    ("C", "Z"): 3,
}

# Dictionary mapping needed selection based on given outcome
SELECTION_MAP = {
    ("A", "X"): "Z",    # Scissors looses over rock
    ("A", "Y"): "X",    # Rock draws with rock
    ("A", "Z"): "Y",    # Paper wins over rock

    ("B", "X"): "X",    # Rock looses over paper
    ("B", "Y"): "Y",    # Paper draws with paper
    ("B", "Z"): "Z",    # Scissors wins over paper

    ("C", "X"): "Y",    # Paper looses over Scissors
    ("C", "Y"): "Z",    # Scissors draws with Scissors
    ("C", "Z"): "X",    # Rock wins over Scissors
}

# Part 1 solution : 
def part_1():
    data = read_lines_sep("input.txt", sep=" ", f=str)

    return sum(RULES[(x, y)] + PICK_SCORE[y] for x, y in data)

# Part 2 solution : 
def part_2():
    data = read_lines_sep("input.txt", sep=" ", f=str)
    return sum(RULES[(x, SELECTION_MAP[(x, y)])] + PICK_SCORE[SELECTION_MAP[(x, y)]] for x, y in data)


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
