import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    return sum(Snafu(s) for s in read_lines(filename, f=str))

# Part 2 solution : 
def part_2():
    return None

class Snafu:
    def __init__(self, value):
        self.value = value
        self.MAP = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
        self.int_value = self.snafu_to_dec()

    def __add__(self, other):
        if isinstance(other, Snafu):
            return Snafu(self.dec_to_snafu(self.int_value + other.int_value))
        if isinstance(other, int):
            return Snafu(self.dec_to_snafu(self.int_value + other))

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return self.value

    def snafu_to_dec(self):
        return sum(self.MAP[digit] * 5**i for i, digit in enumerate(self.value[::-1]))

    def dec_to_snafu(self, n):
        return "" if n == 0 else self.dec_to_snafu((n+2) // 5) + "=-012"[(n+2) % 5]

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
