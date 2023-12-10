from collections import deque

neighbor_offsets = set([(0, -1), (1, 0), (0, 1), (-1, 0)])
neighbor_offset_map = { '|': set([(0, -1), (0, 1)]), '-': set([(-1, 0), (1, 0)]), 'L': set([(0, -1), (1, 0)]), 'J': set([(0, -1), (-1, 0)]), '7': set([(0, 1), (-1, 0)]), 'F': set([(0, 1), (1, 0)]) }

pipe_map = {}
distance_map = {}

def replace_start(start_pos: tuple[int, int]):
    start_x, start_y = start_pos
    confirmed_neighbors = set()
    for x_offset, y_offset in neighbor_offsets:
        neighbor_x = start_x + x_offset
        neighbor_y = start_y + y_offset
        if neighbor_x < 0 or neighbor_y < 0 or (neighbor_x, neighbor_y) not in pipe_map:
            continue
        char = pipe_map[(neighbor_x, neighbor_y)]
        neighbor_neighbors = [(neighbor_x + x_offset, neighbor_y + y_offset) for x_offset, y_offset in neighbor_offset_map[char]]
        if start_pos in neighbor_neighbors:
            confirmed_neighbors.add((x_offset, y_offset))
    for key, offset in neighbor_offset_map.items():
        if confirmed_neighbors == offset:
            print(f'S on pos {start_pos} replaced with {key}')
            pipe_map[start_pos] = key

def parse_input(filename: str):
    start_pos: tuple[int, int]
    with open(filename, 'r') as file:
        for y, line in enumerate(file.readlines()):
            line = line.strip()
            for x, char in enumerate(line):
                if char == '.':
                    continue
                if char == 'S':
                    start_pos = (x, y)
                pipe_map[(x, y)] = char
    replace_start(start_pos)
    return start_pos

def calc_distance_map(start_pos: tuple[int, int]):
    distance_map[start_pos] = 0
    candidates = deque([start_pos])
    furthest_distance = 0
    while candidates:
        current_pos = candidates.popleft()
        x, y = current_pos
        current_char = pipe_map[current_pos]
        neighbors = [(x + x_offset, y + y_offset) for x_offset, y_offset in neighbor_offset_map[current_char]]
        for neighbor in neighbors:
            if neighbor in distance_map:
                continue
            distance = distance_map[current_pos] + 1
            distance_map[neighbor] = distance
            furthest_distance = max(furthest_distance, distance)
            candidates.append(neighbor)
    return furthest_distance

start_pos = parse_input('input-10')
furthest_distance = calc_distance_map(start_pos)
print(furthest_distance)
