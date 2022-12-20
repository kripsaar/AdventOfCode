
class Cube:
    def __init__(self, coords) -> None:
        self.coords = coords
        self.neighbors = []

    def distance(self, other):
        x, y, z = self.coords
        ox, oy, oz = other.coords
        return (abs(x - ox) + abs(y - oy) + abs(z - oz))

    def find_neighbors(self, cubes: list):
        for cube in cubes:
            if self == cube or cube in self.neighbors:
                continue
            if self.distance(cube) == 1:
                self.neighbors.append(cube)
                cube.neighbors.append(self)
    
    def get_open_sides(self):
        return 6 - len(self.neighbors)


def parse_input(filename: str):
    cubes = []
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            line = line.strip()
            x, y, z = line.split(',')
            cubes.append(Cube((int(x), int(y), int(z))))
    for cube in cubes:
        cube.find_neighbors(cubes)
    return cubes

filename = 'input-18'
cubes = parse_input(filename)

area = 0
for cube in cubes:
    area += cube.get_open_sides()

print(f"Surface area = {area}")