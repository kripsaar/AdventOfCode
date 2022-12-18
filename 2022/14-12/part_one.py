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
    else:
        y_range = range(y_from, y_to + 1)

    for x in x_range:
        if x not in cave:
            cave[x] = SortedList()
        col = cave[x]
        for y in y_range:
            if y not in col:
                col.add(y)

def parse_input(filename: str):
    cave = dict()
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
        # there can be no intersection -> sand falls forever
        return False
    col: SortedList = cave[x]
    index = col.bisect_left(y)
    if index >= len(col):
        # no intersection -> sand falls forever
        return False
    intersect_y = col[index]

    # check if left free -> fall left
    if (x - 1) not in cave or (intersect_y) not in cave[x - 1]:
        return fall((x - 1, intersect_y), cave)

    # else check if right free -> fall right
    if (x + 1) not in cave or (intersect_y) not in cave[x + 1]:
        return fall((x + 1, intersect_y), cave)

    # else place sand in map -> return true
    cave[x].add(intersect_y - 1)
    return True

filename = 'input-14'
cave = parse_input(filename)
sand_ingress = (500,0)

sand_count = 0
while fall(sand_ingress, cave):
    sand_count += 1

print(sand_count)