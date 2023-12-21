from enum import Enum

min_x = 0
min_y = 0

y_length = 0
x_length = 0

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Instruction:
    def __init__(self, direction: Direction, distance: int, color: str) -> None:
        self.direction = direction
        self.distance = distance
        self.color = color

    def __repr__(self) -> str:
        return f'{self.direction.name} {self.distance} ({self.color})'

def parse_input(filename: str):
    dig_plan = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            dir_str, distance_str, color = line.split()
            direction: Direction
            if dir_str == 'U':
                direction = Direction.UP
            elif dir_str == 'L':
                direction = Direction.LEFT
            elif dir_str == 'R':
                direction = Direction.RIGHT
            else:
                direction = Direction.DOWN
            dig_plan.append(Instruction(direction, int(distance_str), color.strip('()')))
    return dig_plan

def print_lagoon(lagoon_map: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    lines = []
    for y in range(min_y, y_length):
        line = ''
        for x in range(min_x, x_length):
            if (x, y) in lagoon_map:
                line += '#'
            else:
                line += '.'
        lines.append(line + '\n')
        print(line)
    with open('lagoon_map', 'w') as file:
        file.writelines(lines)

def dig_trenches(dig_plan: list[Instruction]) -> dict[tuple[int, int], str]:
    lagoon_map = {(0, 0): '#ffffff'}
    x = 0
    y = 0
    global min_x
    global min_y
    global x_length
    global y_length
    for instruction in dig_plan:
        x_offset, y_offset = instruction.direction.value
        for idx in range(instruction.distance):
            x += x_offset
            y += y_offset
            lagoon_map[(x, y)] = instruction.color
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            x_length = max(x_length, x + 1)
            y_length = max(y_length, y + 1)
    return lagoon_map

def dig_out_interior(lagoon_map: dict[tuple[int, int], str]):
    new_lagoon_map = lagoon_map.copy()
    white = '#ffffff'
    for y in range(min_y, y_length):
        inside = False
        passing = False
        enter_below = False
        enter_above = False
        for x in range(min_x, x_length):
            hit = (x, y) in lagoon_map
            if hit:
                if not passing:
                    passing = True
                    if (x, y - 1) in lagoon_map and not (x, y + 1) in lagoon_map:
                        enter_above = True
                    elif (x, y + 1) in lagoon_map and not (x, y - 1) in lagoon_map:
                        enter_below = True
                continue
            if passing:
                passing = False
                if enter_above and (x - 1, y - 1) in lagoon_map and not (x - 1, y + 1) in lagoon_map:
                    pass
                elif enter_below and (x - 1, y + 1) in lagoon_map and not (x - 1, y - 1) in lagoon_map:
                    pass
                else:
                    inside = not inside
                enter_above = False
                enter_below = False
            if inside:
                new_lagoon_map[(x, y)] = white
    return new_lagoon_map

def count_volume(lagoon_map: dict[tuple[int, int], str]) -> int:
    return len(lagoon_map)

dig_plan = parse_input('input-18')
lagoon_map = dig_trenches(dig_plan)
# print_lagoon(lagoon_map)
# print()
lagoon_map = dig_out_interior(lagoon_map)
# print_lagoon(lagoon_map)

print(count_volume(lagoon_map))