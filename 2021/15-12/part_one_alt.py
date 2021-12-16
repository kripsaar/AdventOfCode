import bisect
import queue

cave_map = []
distance = {}
path = {(0,0): []}
working_list = []
visited = []

def parse_input(filename: str):
    global cave_map
    global distance
    with open(filename, mode="r") as input:
        lines = [[int(char) for char in line.strip()] for line in input.readlines()]
        y_len = len(lines)
        x_len = len(lines[0])
        for x in range(x_len):
            if len(cave_map) <= x:
                cave_map.append([])
            for y in range(y_len):
                cave_map[x].append(lines[y][x])
                distance[(x, y)] = float('inf')
    distance[(0,0)] = 0
    working_list.append((0,0))

def print_map():
    global cave_map
    x_len = len(cave_map)
    y_len = len(cave_map[0])
    for y in range(y_len):
        line = ""
        for x in range(x_len):
            line += str(cave_map[x][y])
        print(line)

def get_neighbors(point):
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    points = [(point[0] + x, point[1] + y) for x, y in moves]
    return list(filter(lambda point: point[0] >= 0 and point[0] < len(cave_map) and point[1] >= 0 and point[1] < len(cave_map[0]) and point not in visited, points))

def print_path(dest_point):
    global cave_map
    x_len = len(cave_map)
    y_len = len(cave_map[0])
    res = ""
    for y in range(y_len):
        line = ""
        for x in range(x_len):
            point = str(cave_map[x][y])
            point_str = f"[{point}]" if (x, y) in path[dest_point] else f" {point} "
            line += point_str
        res += "\n" + line
    print(res[1:])

parse_input("input-15")

target = (len(cave_map) - 1, len(cave_map[0]) -1)
while len(working_list) > 0:
    current = working_list.pop(0)
    if current == target:
        print_path(current)
        print()
        print(f"Path cost: {distance[current]}")
        break
    visited.append(current)
    neighbors = get_neighbors(current)
    for neighbor in neighbors:
        alt = distance[current] + cave_map[neighbor[0]][neighbor[1]]
        if alt < distance[neighbor]:
            distance[neighbor] = alt
            path[neighbor] = path[current] + [current]
            if neighbor in working_list:
                working_list.remove(neighbor)
            bisect.insort(working_list, neighbor, key=(lambda x: distance[x]))
