
def parse_line(line: str, map):
    start, end = [[int(item) for item in coord.split(",")] for coord in line.strip().replace(" ", "").split("->")]
    
    # Find all x
    all_x = list(range(min(start[0], end[0]), max(start[0], end[0]) + 1))
    if end[0] < start[0]:
        all_x = list(reversed(all_x))

    # Find all y
    all_y = list(range(min(start[1], end[1]), max(start[1], end[1]) + 1))
    if end[1] < start[1]:
        all_y = list(reversed(all_y))

    # Diagonals
    if len(all_x) > 1 and len(all_y) > 1:
        for index in range(len(all_x)):
            x = all_x[index]
            y = all_y[index]
            if (x, y) not in map:
                map[(x, y)] = 0
            map[(x, y)] += 1

    # Horizontal
    elif len(all_x) > 1:
        y = all_y[0]
        for x in all_x:
            if (x, y) not in map:
                map[(x, y)] = 0
            map[(x, y)] += 1

    # Vertical
    else:
        x = all_x[0]
        for y in all_y:
            if (x, y) not in map:
                map[(x, y)] = 0
            map[(x, y)] += 1

def print_map(map: dict):
    x_list = [item[0] for item in map.keys()]
    y_list = [item[1] for item in map.keys()]
    max_x = max(x_list)
    max_y = max(y_list)
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) not in map:
                line = line + "."
            else:
                line = line + str(map[(x, y)])
        print(line)

def count_overlapping_points(map: dict):
    return len(list(filter(lambda value: value > 1, map.values())))

map = {}
with open("input-05", mode="r") as input:
    for line in input:
        parse_line(line, map)

# print_map(map)

print(f"Overlapping points: {count_overlapping_points(map)}")