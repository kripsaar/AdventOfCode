from collections import deque

neighbor_offsets = set([(0, -1), (1, 0), (0, 1), (-1, 0)])
neighbor_offset_map = { '|': set([(0, -1), (0, 1)]), '-': set([(-1, 0), (1, 0)]), 'L': set([(0, -1), (1, 0)]), 'J': set([(0, -1), (-1, 0)]), '7': set([(0, 1), (-1, 0)]), 'F': set([(0, 1), (1, 0)]) }

pipe_map = {}
distance_map = {}
max_x = 0
max_y = 0

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
    global max_x
    global max_y
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
                max_x = max(max_x, x)
            max_y = max(max_y, y)
    replace_start(start_pos)
    return start_pos

def print_pipe_map():
    for y in range(max_y + 1):
        line = ''
        for x in range(max_x + 1):
            if (x, y) not in pipe_map:
                line += ' '
                continue
            line += pipe_map[(x, y)]
        print(line)

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

def clear_junk():
    positions_in_map = set(pipe_map.keys())
    for key in positions_in_map:
        if key not in distance_map:
            del pipe_map[key]

def is_in_loop(pos: tuple[int, int]) -> bool:
    if pos in pipe_map:
        # Pipe bits of the loop are not enclosed in the loop
        return False
    intersection_count = 0
    x, y = pos
    previous_corner = ''
    for x_offset in range(1, max_x + 1):
        new_x = x + x_offset
        if (new_x, y) not in pipe_map:
            continue
        hit = pipe_map[(new_x, y)]
        if hit == '-':
            continue
        if hit == 'L' or hit == 'F':
            previous_corner = hit
            continue
        if hit == 'J':
            if previous_corner == 'F':
                previous_corner = ''
            if previous_corner == 'L':
                previous_corner = ''
                continue
        if hit == '7':
            if previous_corner == 'L':
                previous_corner = ''
            if previous_corner == 'F':
                previous_corner = ''
                continue
        intersection_count += 1
    if intersection_count % 2 == 1:
        return True
    else:
        return False


def explore():
    enclosed_count = 0
    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if is_in_loop((x, y)):
                enclosed_count += 1
    return enclosed_count


start_pos = parse_input('input-10')
furthest_distance = calc_distance_map(start_pos)
print_pipe_map()
clear_junk()
print()
print_pipe_map()

enclosed_count = explore()
print(enclosed_count)
