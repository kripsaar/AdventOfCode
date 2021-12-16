import bisect
import time

cave_map = {}
distance = {}
score = {}
path = {(0,0): []}
working_list = []
visited = []
x_len = 0
y_len = 0

def parse_input(filename: str):
    global cave_map
    global distance
    global x_len
    global y_len
    with open(filename, mode="r") as input:
        lines = [[int(char) for char in line.strip()] for line in input.readlines()]
        y_len = len(lines)
        x_len = len(lines[0])
        for x in range(x_len):
            for y in range(y_len):
                cave_map[(x,y)] = lines[y][x]
                distance[(x, y)] = float('inf')
                score[(x, y)] = float('inf')
    distance[(0,0)] = 0
    score[(0,0)] = 0
    working_list.append((0,0))

def mod_10(value):
    if value > 9:
        return value - 9
    return value


def expand_cave_map():
    global cave_map
    global x_len
    global y_len
    old_x_len = x_len
    old_y_len = y_len
    x_len = 5 * x_len
    y_len = 5 * y_len
    for i in range(0, 6):
        for j in range(0, 6):
            for x in range(old_x_len):
                for y in range(old_y_len):
                    point = (x + i * old_x_len, y + j * old_y_len)
                    cave_map[point] = mod_10((cave_map[(x, y)] + i + j))
                    distance[point] = float("inf")
                    score[point] = float("inf")
    distance[(0,0)] = 0
    score[(0,0)] = 0


def print_map():
    global cave_map
    global x_len
    global y_len
    for y in range(y_len):
        line = ""
        for x in range(x_len):
            line += str(cave_map[(x,y)])
        print(line)

def get_neighbors(point):
    global x_len
    global y_len
    moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    points = [(point[0] + x, point[1] + y) for x, y in moves]
    return list(filter(lambda point: point[0] >= 0 and point[0] < x_len and point[1] >= 0 and point[1] < y_len, points))

def print_path(dest_point):
    global cave_map
    global x_len
    global y_len
    res = ""
    for y in range(y_len):
        line = ""
        for x in range(x_len):
            point = str(cave_map[(x,y)])
            point_str = f"[{point}]" if (x, y) in path[dest_point] else f" {point} "
            line += point_str
        res += "\n" + line
    print(res[1:])

def manhattan_distance(point):
    return (x_len - point[0] - 1) + (y_len - point[1] - 1)

parse_input("input-15")
expand_cave_map()

start = time.perf_counter_ns()
target = (x_len - 1, y_len -1)
print(target)
while len(working_list) > 0:
    current = working_list.pop(0)
    if current == target:
        print()
        print(f"Path cost: {distance[current]}")
        end = time.perf_counter_ns()
        duration = int((end - start) / 1_000_000)
        print(f"Duration: {duration}ms")
        break
    visited.append(current)
    neighbors = get_neighbors(current)
    for neighbor in neighbors:
        alt = distance[current] + cave_map[(neighbor[0], neighbor[1])]
        if alt < distance[neighbor]:
            distance[neighbor] = alt
            score[neighbor] = alt + manhattan_distance(neighbor)
            path[neighbor] = path[current] + [current]
            if neighbor not in working_list:
                bisect.insort(working_list, neighbor, key=(lambda x: score[x]))
