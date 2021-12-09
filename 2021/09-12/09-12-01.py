def is_low_point(x: int, y: int, map: list):
    neighbors = []
    if x > 0:
        neighbors.append(map[y][x - 1])
    if x < len(map[0]) - 1:
        neighbors.append(map[y][x + 1])
    if y > 0:
        neighbors.append(map[y - 1][x])
    if y < len(map) - 1:
        neighbors.append(map[y + 1][x])
    # print(f"Point ({x},{y}) = {map[y][x]}")
    # print(f"Neighbors: {neighbors}")
    if all([neighbor > map[y][x] for neighbor in neighbors]):
        # print("Low point found!")
        # print()
        return True
    else:
        # print()
        return False

def find_low_points_for_row(y, row, map, low_point_risks):
    for x in range(len(row)):
        if is_low_point(x, y, map):
            low_point_risks.append(map[y][x] + 1)

def parse_input(filename: str):
    map = []
    low_point_risks = []
    with open(filename, mode="r") as input:
        for line in input:
            row = [int(char) for char in line.strip()]
            map.append(row)
            if len(map) == 1:
                continue
            y = len(map) - 2
            find_low_points_for_row(y, row, map, low_point_risks)
        y = len(map) - 1
        find_low_points_for_row(y, map[y], map, low_point_risks)
    return map, low_point_risks
        
point_map, low_point_risks = parse_input("input-09")
print(sum(low_point_risks)) 