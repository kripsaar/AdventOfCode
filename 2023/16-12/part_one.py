from enum import Enum

y_length = 0
x_length = 0

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

def parse_input(filename: str):
    global y_length
    global x_length
    layout = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        y_length = len(lines)
        x_length = len(lines[0])
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                layout[(x, y)] = char
    return layout

def print_visited(visited):
    for y in range(y_length):
        line = ''
        for x in range(x_length):
            if (x, y) in visited:
                line += '#'
            else:
                line += '.'
        print(line)

def step(pos: tuple[int, int], direction = Direction):
    x, y = pos
    return (x + direction.value[0], y + direction.value[1])

def follow_ray(layout: dict[tuple[int, int], str], pos = (0, 0), direction: Direction = Direction.RIGHT, visited: dict[tuple[int, int], set[Direction]] = {}):
    while True:
        if pos not in layout:
            break
        if pos not in visited:
            visited[pos] = set()
        elif direction in visited[pos]:
            break
        visited[pos].add(direction)
        if layout[pos] == '.':
            pos = step(pos, direction)
            continue
        if layout[pos] == '\\':
            if direction == Direction.UP:
                direction = Direction.LEFT
            elif direction == Direction.DOWN:
                direction = Direction.RIGHT
            elif direction == Direction.LEFT:
                direction = Direction.UP
            elif direction == Direction.RIGHT:
                direction = Direction.DOWN
            pos = step(pos, direction)
            continue
        if layout[pos] == '/':
            if direction == Direction.UP:
                direction = Direction.RIGHT
            elif direction == Direction.DOWN:
                direction = Direction.LEFT
            elif direction == Direction.LEFT:
                direction = Direction.DOWN
            elif direction == Direction.RIGHT:
                direction = Direction.UP
            pos = step(pos, direction)
            continue
        if layout[pos] == '|':
            if direction == Direction.UP or direction == Direction.DOWN:
                pos = step(pos, direction)
                continue
            follow_ray(layout, step(pos, Direction.UP), Direction.UP, visited)
            follow_ray(layout, step(pos, Direction.DOWN), Direction.DOWN, visited)
            break
        if layout[pos] == '-':
            if direction == Direction.LEFT or direction == Direction.RIGHT:
                pos = step(pos, direction)
                continue
            follow_ray(layout, step(pos, Direction.LEFT), Direction.LEFT, visited)
            follow_ray(layout, step(pos, Direction.RIGHT), Direction.RIGHT, visited)
            break
    return visited

layout = parse_input('input-16')
visited = follow_ray(layout)
print(len(visited.keys()))
