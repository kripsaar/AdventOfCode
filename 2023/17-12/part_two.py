from bisect import insort
from collections import deque

x_length = 0
y_length = 0

class Path:
    def __init__(self, cost, nodes: list[tuple[int, int]], last_direction: tuple[int, int], direction_count: int) -> None:
        self.cost = cost
        self.nodes = nodes
        self.last_direction = last_direction
        self.direction_count = direction_count

    def __repr__(self) -> str:
        result = f'[{self.cost}] - '
        for node in self.nodes:
            result += f'{node}, '
        return result.strip(', ')

def parse_input(filename: str):
    global x_length
    global y_length
    cost_map = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        y_length = len(lines)
        x_length = len(lines[0].strip())
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                cost_map[(x, y)] = int(char)
    return cost_map

def print_path(cost_map: dict[tuple[int, int], int], path: Path):
    for y in range(y_length):
        line = ''
        for x in range(x_length):
            if (x, y) in path.nodes:
                line += '#'
            else:
                line += str(cost_map[(x, y)])
        print(line)

def generate_candidates(cost_map: dict[tuple[int, int], int], current_path: Path) -> list[Path]:
    candidates = []
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    x, y = current_path.nodes[-1]
    for x_offset, y_offset in directions:
        direction = (x_offset, y_offset)
        new_node = (x + x_offset, y + y_offset)
        if new_node not in cost_map:
            continue
        if current_path.last_direction != direction and current_path.direction_count < 4:
            continue
        if current_path.last_direction == direction and current_path.direction_count == 10:
            continue
        if new_node in current_path.nodes:
            continue
        new_path_nodes = current_path.nodes.copy()
        new_path_nodes.append(new_node)
        count = 1
        if current_path.last_direction == direction:
            count = current_path.direction_count + 1
        new_path = Path(current_path.cost + cost_map[new_node], new_path_nodes, direction, count)
        candidates.append(new_path)
    return candidates

def get_distance(from_node: tuple[int, int], to_node: tuple[int, int]) -> int:
    return abs(to_node[0] - from_node[0]) + abs(to_node[1] - from_node[1])

def find_path(cost_map: dict[tuple[int, int], int]) -> Path:
    goal = (x_length - 1, y_length - 1)
    init_path = Path(0, [(0, 0)], (1, 1), 5)
    candidates = deque([init_path])
    visited = {}
    paths_tested = 0
    while candidates:
        paths_tested += 1
        current_path = candidates.popleft()
        last_node = current_path.nodes[-1]
        if last_node == goal and current_path.direction_count >= 4:
            print(f'Paths tested: {paths_tested}')
            return current_path
        state = (last_node, current_path.last_direction, current_path.direction_count)
        if state in visited and visited[state] <= current_path.cost:
            continue
        visited[state] = current_path.cost
        
        new_candidates = generate_candidates(cost_map, current_path)
        for candidate in new_candidates:
            insort(candidates, candidate, key = lambda x: x.cost + (2 * get_distance(x.nodes[-1], goal)))
    return None

cost_map = parse_input('input-17')
path = find_path(cost_map)
print(path.cost)