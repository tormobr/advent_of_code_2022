import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    data = parse_data()
    target_row = 2000000
    not_valid = set()

    for sensor_x, sensor_y, beacon_x, beacon_y in data:
        distance_to_beacon = manhatten(beacon_x, sensor_x, beacon_y, sensor_y)
        distance_to_row = abs(target_row - sensor_y)
        spare_distance = distance_to_beacon - distance_to_row

        x_range = set(range(sensor_x - spare_distance, sensor_x + spare_distance))
        not_valid |= x_range

    return len(not_valid)

# Part 2 solution : 
def part_2():
    data = parse_data()
    sensors = {}

    for sensor_x, sensor_y, beacon_x, beacon_y in data:
        sensors[(sensor_x, sensor_y)] = manhatten(beacon_x, sensor_x, beacon_y, sensor_y)

    return find_hidden_beacon(sensors)

def find_hidden_beacon(sensors):
    grid_size = 4000000
    for (sensor_x, sensor_y), distance in sensors.items():
        l_x, l_y = sensor_x - distance-1, sensor_y
        r_x, r_y = sensor_x + distance+1, sensor_y

        borders = ([(l_x + dxy, l_y - dxy) for dxy in range(distance+2)]
                 + [(l_x + dxy, l_y + dxy) for dxy in range(distance+2)]
                 + [(r_x - dxy, r_y - dxy) for dxy in range(distance+2)]
                 + [(r_x - dxy, r_y + dxy) for dxy in range(distance+2)])

        for border_x, border_y in borders:
            if inside_bounds(grid_size, border_x, border_y) and outside_diamond(sensors, border_x, border_y):
                return border_x * 4000000 + border_y


def parse_data():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"
    data = read_lines(filename, f=str)
    return [tuple(ints(line)) for line in data]

def outside_diamond(sensors, x, y):
    return not any(manhatten(x, sensor_x, y, sensor_y) <= distance for (sensor_x, sensor_y), distance in sensors.items())

def inside_bounds(grid_size, x, y):
    return x >= 0 and x < grid_size and y >= 0 and y < grid_size

def manhatten(x1, x2, y1, y2):
    return abs(x2 - x1) + abs(y2 - y1)


if __name__ == "__main__":
    pretty_print(part_1(), part_2())
