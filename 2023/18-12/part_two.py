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
    def __init__(self, direction: Direction, distance: int) -> None:
        self.direction = direction
        self.distance = distance

    def __repr__(self) -> str:
        return f'{self.direction.name} {self.distance}'

def decode_color(color: str):
    distance = int(color[:5], 16)
    dir_str = color[5]
    direction: Direction
    if dir_str == '0':
        direction = Direction.RIGHT
    elif dir_str == '1':
        direction = Direction.DOWN
    elif dir_str == '2':
        direction = Direction.LEFT
    elif dir_str == '3':
        direction = Direction.UP
    else:
        raise Exception('Direction encoding wrong!')
    return distance, direction

def parse_input(filename: str):
    dig_plan = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            dir_str, distance_str, color = line.split()
            distance, direction = decode_color(color.strip('()').strip('#'))
            dig_plan.append(Instruction(direction, distance))
    return dig_plan

def generate_edges(dig_plan: list[Instruction]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    x = 0
    y = 0
    previous_node = (0, 0)
    edges = []
    for instruction in dig_plan:
        x_offset, y_offset = instruction.direction.value
        x += x_offset * instruction.distance
        y += y_offset * instruction.distance
        edges.append((previous_node, (x, y)))
        previous_node = (x, y)
    return edges

def edge_length(edge: tuple[tuple[int, int], tuple[int, int]]):
    node_a, node_b = edge
    x_a, y_a = node_a
    x_b, y_b = node_b
    result = abs(x_b - x_a) + abs(y_b - y_a)
    return result

def shoelace(edges: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    shoelace_sum = sum([edge[0][0] * edge[1][1] - edge[1][0] * edge[0][1] for edge in edges])
    return abs(shoelace_sum)/2

def count_exterior_points(edges: list[tuple[tuple[int, int], tuple[int, int]]]) -> int:
    return sum([edge_length(edge) for edge in edges])

def pick_interior(area: int, exterior_points: int):
    return int(area - (exterior_points / 2) + 1)

dig_plan = parse_input('input-18')
edges = generate_edges(dig_plan)
area = shoelace(edges)
exterior_points = count_exterior_points(edges)
interior_points = pick_interior(area, exterior_points)
print(exterior_points + interior_points)