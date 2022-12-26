from collections import deque, defaultdict
import sys
sys.path.insert(0,'..')
from advent_lib import *

# Part 1 solution : 
def part_1():
    best, _ = solve(m=30)
    return best

# Part 2 solution : 
def part_2():
    _, paths = solve(m=26)

    # Returns the higest sum of preasure of two paths that are disjoint
    return max(p1 + p2 for p1, nodes in paths for p2, nodes2 in paths if nodes.isdisjoint(nodes2))

def solve(m):
    neighbors, flowrates = parse_data()
    graph = create_graph(neighbors, flowrates)

    best = 0
    q = deque([("AA", 0, m, set())])
    paths = []
    while q:
        valve, preasure, minutes, visited = q.popleft()

        # Update current sate variables and check if new best is found
        preasure += minutes * flowrates[valve]
        minutes -= 1
        best = preasure if preasure > best else best

        visited.add(valve)
        if minutes == 1:
            to_add = visited.copy()
            to_add.remove("AA") # Remove "AA" from path to be able to identify disjoint paths
            paths.append((preasure, to_add))


        # Iterate neighbors and add them to queue
        for n, cost in graph[valve]:
            # if minutes left is 1 or less no more flow is gained from moving there
            if minutes - cost > 1 and n not in visited:
                q.append((n, preasure, minutes - cost, visited.copy()))

    return best, paths

def parse_data():
    filename = sys.argv[1] if len(sys.argv) == 2 else "input.txt"

    flowrates = defaultdict(int)
    neighbors = defaultdict(dict)
    data = read_lines(filename, f=str)
    for line in data:
        neighbor_valves = [x for x in re.findall(r"[A-Z][A-Z]", line)]
        from_valve = neighbor_valves[0]
        neighbors[from_valve] = neighbor_valves[1:]
        flowrates[from_valve] = ints(line)[0]

    return neighbors, flowrates

# Builds a graph with every possible next node from current
# and the number of steps required to get there
def create_graph(neighbors, flowrates):
    graph = defaultdict(list)
    for key in neighbors.keys():
        v = set()
        q = deque([(key, 1, v)])
        while q:
            current_key, steps, visited = q.popleft()
            if current_key in visited:
                continue

            visited.add(current_key)
            for n in neighbors[current_key]:
                if n not in [x for x, _ in graph[key]] and flowrates[n] != 0 and n != key:
                    graph[key].append((n, steps))
                q.append((n, steps + 1, visited.copy()))
    return graph


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
