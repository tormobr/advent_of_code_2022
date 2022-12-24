from collections import defaultdict
import sys
sys.path.insert(0,'..')
from advent_lib import *


DIRECTIONS = {
    "N": (0, -1),
    "S": (0, 1),
    "W": (-1, 0),
    "E": (1, 0),
    "NW": (-1, -1),
    "NE": (1, -1),
    "SE": (1, 1),
    "SW": (-1, 1)
}

TURNS = [
    (DIRECTIONS["N"], [DIRECTIONS["N"], DIRECTIONS["NE"], DIRECTIONS["NW"]]),
    (DIRECTIONS["S"], [DIRECTIONS["S"], DIRECTIONS["SE"], DIRECTIONS["SW"]]),
    (DIRECTIONS["W"], [DIRECTIONS["W"], DIRECTIONS["NW"], DIRECTIONS["SW"]]),
    (DIRECTIONS["E"], [DIRECTIONS["E"], DIRECTIONS["NE"], DIRECTIONS["SE"]])
]


# Part 1 solution : 
def part_1(rounds=10):
    return solve(rounds=10)

# Part 2 solution : 
def part_2():
    # Just run same same solving algorithm with high number of rounds
    # and "hope" for early exit due to no movement
    return solve(rounds=10000)

def solve(rounds=10):
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines_sep(filename, sep="", f=str)
    positions = set((x, y) for y, row in enumerate(data) for x, elem in enumerate(row) if elem == "#")

    turn_index = 0  # The current first pick of the rules
    for r in range(1, rounds +1):

        # Dictionary with target x, y and key and value as an array over current elves
        # that wants to move there
        D = defaultdict(list)   
        for x, y in positions:
            # All surrounding squares are free, we are not moving
            if all((x + dx, y + dy) not in positions for dx, dy in DIRECTIONS.values()):
                D[(x, y)].append((x, y))
                continue

            # Ty moving according to rules
            for i in range(len(TURNS)):
                (target_x, target_y), tests = TURNS[(turn_index + i) % len(TURNS)]
                if all((x + dx, y + dy) not in positions for dx, dy in tests):
                    D[(x + target_x, y + target_y)].append((x, y))
                    break

            # If no move was possible we stay at current position
            else:
                D[(x, y)].append((x, y))

        # Move elves according to desire and considder rules that 2 elves can me to same square
        new_positions = set()
        for new_xy, elves_current_xy in D.items():
            new_positions |= {(new_xy)} if len(elves_current_xy) == 1 else set(elves_current_xy)

        # If nothing moves, return the current round
        if new_positions == positions:
            return r
            
        # Update indecies and positions
        turn_index = (turn_index + 1) % len(TURNS)
        positions = new_positions
                
    min_x, max_x = min(positions, key=lambda x: x[0])[0], max(positions, key=lambda x: x[0])[0]
    min_y, max_y = min(positions, key=lambda x: x[1])[1], max(positions, key=lambda x: x[1])[1]

    return sum((x, y) not in positions for y in range(min_y, max_y+1) for x in range(min_x, max_x+1))


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
