from copy import deepcopy
from dataclasses import dataclass
import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    return solve()

# Part 2 solution : 
def part_2():
    return solve(factor=811589153, mixings=10)

def solve(factor=1, mixings=1):
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"

    # Store list of objects and information about index of zero to start
    data = [int(line) for line in open(filename, "r")]
    start_zero_index = data.index(0)
    data = [Num(n*factor, i) for i, n in enumerate(data)]
    og_data = deepcopy(data)

    # Perform mixing 
    for _ in range(mixings):
        for n in og_data:
            pop_index = data.index(n)
            data.pop(pop_index)
            insert_index = get_index(pop_index, n.value, len(data))
            data.insert(insert_index, n)


    # Calculate and return results
    zero_index = data.index(Num(0, start_zero_index))
    a = get_index(1000, zero_index, len(data))
    b = get_index(2000, zero_index, len(data))
    c = get_index(3000, zero_index, len(data))

    return data[a] + data[b] + data[c]

def get_index(value, current_index, length):
    new_index = current_index + value
    # new_inde is less than zero we convert it to positive index
    if new_index < 0:
        return new_index + (length * ((abs(new_index) // length)+1))

    # If index is larger than zero we make sure it doesn't exceed length
    # using modular arithmetic to wrap it
    return new_index % length


# A class to represent a number
# Makes it easier to identify index of elements
# since multiple elements can have same value
@dataclass
class Num:
    value: int
    index: int

    def __add__(self, num):
        if isinstance(num, Num):
            return self.value + num.value
        if isinstance(num, int):
            return self.value + num

    def __radd__(self, num):
        return self.__add__(num)

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
