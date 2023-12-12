import re
from itertools import combinations

class Universe:
    def __init__(self, universe_map: dict, empty_x: list, empty_y: list) -> None:
        pass

class Galaxy:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos

    def __repr__(self) -> str:
        return f'({self.pos[0]}, {self.pos[1]})'

    def move_x(self):
        self.pos = (self.pos[0] + 1, self.pos[1])

    def move_y(self):
        self.pos = (self.pos[0], self.pos[1] + 1)

def calc_distance(left: Galaxy, right: Galaxy) -> int:
    x_dist = abs(right.pos[0] - left.pos[0])
    y_dist = abs(right.pos[1] - left.pos[1])
    return x_dist + y_dist

def print_universe(universe: list[Galaxy]):
    max_x = 0
    max_y = 0
    universe_map = {}
    for galaxy in universe:
        x, y = galaxy.pos
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        universe_map[(x, y)] = '#'
    for y in range(0, max_y + 1):
        line = ''
        for x in range(0, max_x + 1):
            if (x, y) in universe_map:
                line += '#'
            else:
                line += '.'
        print(line)

def parse_input(filename: str):
    universe = []
    galaxy_x_map = {}
    non_empty_x = set()
    max_x = 0
    with open(filename, 'r') as file:
        y = 0
        for line in file.readlines():
            line = line.strip()
            max_x = len(line)
            if '#' not in line:
                y += 2
                continue
            for x in [idx for idx, char in enumerate(line) if char == '#']:
                non_empty_x.add(x)
                galaxy = Galaxy((x, y))
                universe.append(galaxy)
                if x not in galaxy_x_map:
                    galaxy_x_map[x] = []
                galaxy_x_map[x].append(galaxy)
            y += 1
    empty_x_set = set(range(0, max_x + 1)).difference(non_empty_x)
    for x, galaxies in galaxy_x_map.items():
        smaller_empty_x = filter(lambda empty_x: empty_x < x, empty_x_set)
        for smaller_x in smaller_empty_x:
            for galaxy in galaxies:
                galaxy.move_x()
    return universe

universe = parse_input('input-11')
sum = 0
for left_galaxy, right_galaxy in combinations(universe, 2):
    sum += calc_distance(left_galaxy, right_galaxy)

print(sum)
