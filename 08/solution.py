from functools import reduce
import operator
import numpy as np

import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    data = np.array(read_lines_sep("input.txt", sep="", f=str))

    return sum(is_visible(data, row, col) for row in range(len(data)) for col in range(len(data[row])))

# Part 2 solution : 
def part_2():
    data = np.array(read_lines_sep("input.txt", sep="", f=str))

    scenic_scores = [[total_scenic_score(data, row, col) for col in range(len(data[row]))] for row in range(len(data))]
    return np.max(scenic_scores)

def get_trees(data, row, col):
    return [data[row, col+1:],
            data[row, :col][::-1],
            data[:row, col][::-1],
            data[row+1:, col]]

def is_visible(data, row, col):
    current = data[row, col]
    return any(all(tree < current for tree in trees) for trees in get_trees(data, row, col))

def total_scenic_score(data, row, col):
    current = data[row, col]
    return reduce(operator.mul, [scenic_score(data, row, col, trees) for trees in get_trees(data, row, col)])

def scenic_score(data, row, col, trees):
    return next((i for i in range(len(trees)) if trees[i] >= data[row, col]), len(trees) - 1) + 1

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
