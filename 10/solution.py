import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    data = read_lines("input.txt", f=str)
    cycle, x, current_index, tot = 1, 1, 0, 0

    while current_index < len(data):
        line = data[current_index]
        command = line.split()[0]

        if cycle == 20 or (20 + cycle) % 40 == 0:
            tot += x * cycle

        if command == "addx":
            cycle += 1
            if cycle == 20 or (20 + cycle) % 40 == 0:
                tot += x * cycle

            x += int(line.split()[1])


        cycle += 1
        current_index += 1

    return tot

# Part 2 solution : 
def part_2():
    data = read_lines("input.txt", f=str)

    center_of_sprite, cycle, current_index = 1, 0, 0
    drawing = ""

    while current_index < len(data):
        line = data[current_index]
        command = line.split()[0]

        # Draw before executing any commands
        drawing = draw(center_of_sprite, cycle, drawing)

        if command == "addx":
            # Add cycle to complete operation, and redraw
            cycle += 1
            drawing = draw(center_of_sprite, cycle, drawing)

            center_of_sprite += int(line.split()[1])

        cycle += 1
        current_index += 1

    return drawing

def draw(center_of_sprite, cycle, drawing):
    if cycle % 40 == 0:
        drawing += "\n"
    return drawing + ("#" if (cycle % 40) in range(center_of_sprite - 1, center_of_sprite + 2) else " ")

if __name__ == "__main__":
    pretty_print(part_1(), part_2())
