class Path:
    def __init__(self, connections: dict, visited: list = ["start"], current_node: str = "start"):
        self.connections = connections
        self.visited = visited
        self.current_node = current_node

    def length(self):
        return len(self.visited)

    def step(self):
        if self.current_node == "end":
            return [self]
        candidates = self.connections[self.current_node]
        paths = []
        for candidate in candidates:
            if candidate.islower() and candidate in self.visited:
                continue
            new_visited = self.visited.copy()
            new_visited.append(candidate)
            paths += Path(self.connections, new_visited, candidate).step()
        return paths

    def print_path(self):
        path_string = ""
        for node in self.visited:
            path_string += node
        print(path_string)


def run(filename: str):
    initial = parse_input(filename)
    result = initial.step()
    print(f"Found {len(result)} paths")
    return len(result)
    # for path in result:
    #     path.print_path()

def parse_input(filename: str):
    connections = {}
    with open(filename, mode="r") as input:
        for line in input:
            left, right = line.strip().split("-")
            if left not in connections:
                connections[left] = []
            if right not in connections:
                connections[right] = []
            connections[left].append(right)
            connections[right].append(left)
    return Path(connections)

run("input-12")