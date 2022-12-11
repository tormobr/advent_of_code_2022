import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    return solve()

# Part 2 solution : 
def part_2():
    return solve(n_knots=10)


# Solves the problem for arbitrary number of knots on the rope
def solve(n_knots=2):
    moves = read_lines_sep("input.txt", sep=" ", f=str)

    knots = [(0, 0)] * n_knots # All knots start on (0, 0)
    visited = set() # Keeps track of places tail has visited

    for direction, steps in moves:
        for i in range(int(steps)):
            # Update the head with the movement
            dy, dx = DIRECTIONS[direction]
            head_y, head_x = knots[-1]
            knots[-1] = (head_y + dy, head_x + dx)

            # Iterate all knots and update their positions
            for j in range(len(knots) - 2, -1, -1):
                knot_y, knot_x = knots[j]
                knot_ahead_y, knot_ahead_x = knots[j+1]
                new_knot_y, new_knot_x = knot_y, knot_x

                # Calculate new knot position based on own position and knot ahead
                if abs(knot_ahead_x - knot_x) > 1 or abs(knot_ahead_y - knot_y) > 1:
                    if knot_ahead_y - knot_y != 0:
                        new_knot_y += 1 if (knot_ahead_y - knot_y) > 0 else -1
                    if knot_ahead_x - knot_x != 0:
                        new_knot_x += 1 if (knot_ahead_x - knot_x) > 0 else -1

                # Update knot position in knot array
                knots[j] = (new_knot_y, new_knot_x)

            visited.add(knots[0])
            
    return len(visited)


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
