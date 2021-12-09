import math

basins = []
point_to_basin_dict = {}
point_map = []

def determine_basin_for_point(x: int, y: int, basin: list = None):
    global basins
    global point_to_basin_dict
    global point_map
    if point_map[y][x] == 9:
        return
    if (x, y) in point_to_basin_dict.keys():
        return
    if basin is None:
        basin = []
        basins.append(basin)
    basin.append((x, y))
    point_to_basin_dict[(x, y)] = basin
    if x > 0:
        determine_basin_for_point(x - 1, y, basin)
    if x < len(point_map[y]) - 1:
        determine_basin_for_point(x + 1, y, basin)
    if y > 0:
        determine_basin_for_point(x, y - 1, basin)
    if y < len(point_map) - 1:
        determine_basin_for_point(x, y + 1, basin)


def determine_basins_for_row(y):
    global point_map
    for x in range(len(point_map[y])):
        determine_basin_for_point(x, y)

def parse_input(filename: str):
    global point_map
    with open(filename, mode="r") as input:
        for line in input:
            row = [int(char) for char in line.strip()]
            point_map.append(row)
        
parse_input("input-09")
for y in range(len(point_map)):
    determine_basins_for_row(y)

basins.sort(key = len, reverse = True)

result = math.prod([len(basin) for basin in basins[0:3]])
print(f"Result: {result}")
