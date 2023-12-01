from itertools import product

class Cube:
    def __init__(self, coords, is_lava) -> None:
        self.coords = coords
        self.neighbors = []
        self.is_lava = is_lava

    def __repr__(self) -> str:
        cube_type = "AIR"
        if self.is_lava:
            cube_type = "LAVA"
        return f"{cube_type}{self.coords}"

    def distance(self, other):
        x, y, z = self.coords
        ox, oy, oz = other.coords
        return (abs(x - ox) + abs(y - oy) + abs(z - oz))

    def generate_air(self, cubes: dict):
        offsets = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
        for offset in offsets:
            neighbor_coords = tuple(map(sum, zip(self.coords, offset)))
            if neighbor_coords not in cubes:
                cubes[neighbor_coords] = Cube(neighbor_coords, False)

    def find_neighbors(self, cubes: dict):
        offsets = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
        for offset in offsets:
            neighbor_coords = tuple(map(sum, zip(self.coords, offset)))
            if neighbor_coords not in cubes:
                continue
            neighbor = cubes[neighbor_coords]
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
            if self not in neighbor.neighbors:
                neighbor.neighbors.append(self)
    
    def purge_air_neighbors(self):
        # print(f"Purging air neighbors with visited = {visited}")
        for neighbor in self.neighbors.copy():
            if neighbor.is_lava:
                continue
            if len(neighbor.neighbors) < 6:
                self.neighbors.remove(neighbor)

    def get_open_sides(self):
        return 6 - len(self.neighbors)


def parse_input(filename: str):
    cubes = dict()
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            line = line.strip()
            x, y, z = line.split(',')
            coords = (int(x), int(y), int(z))
            cubes[coords] = Cube(coords, True)
    lava_cubes_list = list(cubes.values()).copy()

    air_range = 5
    for i in range(0, air_range):
        cubes_list = list(cubes.values()).copy()
        for cube in cubes_list:
            cube.generate_air(cubes)
    for cube in cubes.values():
        cube.find_neighbors(cubes)
    for i in range(0, air_range + 1):
        for cube in cubes.values():
            cube.purge_air_neighbors()
    return cubes

filename = 'input-18'
cubes = parse_input(filename)

area = 0
for cube in cubes.values():
    if cube.is_lava:
        area += cube.get_open_sides()

print(f"Surface area = {area}")