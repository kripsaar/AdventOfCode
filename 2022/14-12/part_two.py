from sortedcontainers import SortedList
from typing import Dict

def parse_line(p_from, p_to, cave):
    x_from, y_from = [int(item) for item in p_from.split(',')]
    x_to, y_to = [int(item) for item in p_to.split(',')]
    x_range = None
    y_range = None
    if x_from > x_to:
        x_range = range(x_to, x_from + 1)
    else:
        x_range = range(x_from, x_to + 1)
    if y_from > y_to:
        y_range = range(y_to, y_from + 1)
        cave[-1] = max(cave[-1], y_from + 2)
    else:
        y_range = range(y_from, y_to + 1)
        cave[-1] = max(cave[-1], y_to + 2)

    for x in x_range:
        if x not in cave:
            cave[x] = SortedList()
        col = cave[x]
        for y in y_range:
            if y not in col:
                col.add(y)

def parse_input(filename: str):
    cave = {-1: 0}
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            line = line.strip()
            points = line.split(' -> ')
            while len(points) > 1:
                p_from = points[0]
                p_to = points[1]
                parse_line(p_from, p_to, cave)
                points = points[1:]
    return cave

def fall(start, cave: dict[SortedList]) -> bool:
    # find next intersection on same x
    x, y = start
    if x not in cave:
        # only floor
        cave[x] = SortedList([cave[-1]])
    col: SortedList = cave[x]
    if y in cave[x]:
        # cave is full, we done
        print(f"Cave is full for {start}")
        return False
    index = col.bisect_left(y)
    if index >= len(col):
        # no intersection -> sand falls forever
        print(f"No intersection for ({x}, {y})")
        return False
    intersect_y = col[index]

    # check if left free -> fall left
    if x - 1 not in cave:
        # only floor
        cave[x - 1] = SortedList([cave[-1]])
    if (intersect_y) not in cave[x - 1]:
        return fall((x - 1, intersect_y), cave)

    # else check if right free -> fall right
    if x + 1 not in cave:
        cave[x + 1] = SortedList([cave[-1]])
    if (intersect_y) not in cave[x + 1]:
        return fall((x + 1, intersect_y), cave)

    # else place sand in map -> return true
    cave[x].add(intersect_y - 1)
    return True

filename = 'input-14'
cave = parse_input(filename)
for key in cave:
    if key == -1:
        continue
    if cave[-1] not in cave[key]:
        cave[key].add(cave[-1])
sand_ingress = (500,0)

sand_count = 0
while fall(sand_ingress, cave):
    sand_count += 1

print(sand_count)