
x_length = 0
y_length = 0

def parse_input(filename: str) -> dict[tuple[int, int], str]:
    global x_length
    global y_length
    rocks = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        y_length = len(lines)
        x_length = len(lines[0].strip())
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == "O" or char == '#':
                    rocks[(x, y)] = char
    return rocks

def print_rocks(rocks: dict[tuple[int, int], str]):
    result = ''
    for y in range(y_length):
        line = ''
        for x in range(x_length):
            if (x, y) not in rocks:
                line += '.'
            else:
                line += rocks[(x, y)]
        result += line + '\n'
    return result.strip()

def tilt(rocks: dict[tuple[int, int], str], direction_offset: tuple[int, int]) -> dict[tuple[int, int], str]:
    tilted_rocks = {}
    y_range = range(y_length)
    x_range = range(x_length)
    if direction_offset[0] > 0 or direction_offset[1] > 0:
        y_range = range(y_length - 1, -1, -1)
        x_range = range(x_length - 1, -1, -1)
    for y in y_range:
        for x in x_range:
            if (x, y) not in rocks:
                continue
            if rocks[(x, y)] == '#':
                tilted_rocks[(x, y)] = rocks[(x, y)]
                continue
            target = (x, y)
            while target[0] >= 0 and target[0] < x_length and target[1] >= 0 and target[1] < y_length:
                next_target = (target[0] + direction_offset[0], target[1] + direction_offset[1])
                if next_target in tilted_rocks or next_target[0] < 0 or next_target[0] >= x_length or next_target[1] < 0 or next_target[1] >= y_length:
                    break
                else:
                    target = next_target
            tilted_rocks[target] = rocks[(x, y)]
    return tilted_rocks

def tilt_north(rocks: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    return tilt(rocks, (0, -1))

def tilt_west(rocks: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    return tilt(rocks, (-1, 0))

def tilt_south(rocks: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    return tilt(rocks, (0, 1))

def tilt_east(rocks: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    return tilt(rocks, (1, 0))

def cycle(rocks: dict[tuple[int, int], str], cycle_count: int = 1) -> dict[tuple[int, int], str]:
    previous_cycle = rocks
    visited_states = {}
    for idx in range(cycle_count):
        north = tilt_north(previous_cycle)
        # print('N:')
        # print_rocks(north)
        # print()
        west = tilt_west(north)
        # print('W:')
        # print_rocks(west)
        # print()
        south = tilt_south(west)
        # print('S:')
        # print_rocks(south)
        # print()
        east = tilt_east(south)
        # print('E:')
        # print_rocks(east)
        # print()
        east_str = print_rocks(east)
        if east_str in visited_states:
            loop_length = idx - visited_states[east_str]
            remaining_cycles = ((cycle_count - (visited_states[east_str] + 1)) % loop_length)
            return cycle(east, remaining_cycles)
        visited_states[east_str] = idx
        previous_cycle = east
    return previous_cycle

def score_rocks(rocks: dict[tuple[int, int], str]) -> int:
    score = 0
    for y in range(y_length):
        for x in range(x_length):
            if (x, y) not in rocks or rocks[(x, y)] == '#':
                continue
            score += y_length - y
    return score

rocks = parse_input('input-14')
cycled_rocks = cycle(rocks, 1_000_000_000)
score = score_rocks(cycled_rocks)
print(score)