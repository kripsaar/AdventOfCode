
def parse_input(filename: str):
    forest = {}
    with open(filename, mode='r') as file:
        y = 0
        x_size = 0
        for line in file.readlines():
            line = line.strip()
            size = len(line)
            x = 0
            while x < size:
                forest[(x, y)] = int(line[x])
                x += 1
            x_size = x
            y += 1
    return forest, x_size, y

def print_forest(forest, x_size, y_size):
    for y in range(0, y_size):
        line = ""
        for x in range(0, x_size):
            line += str(forest[(x, y)])
        print(line)

def calc_score(pos_x, pos_y, forest, x_size, y_size):
    val = forest[(pos_x, pos_y)]
    north = 0
    for y in range(pos_y - 1, -1, -1):
        north += 1
        if not forest[(pos_x, y)] < val:
            break
    south = 0
    for y in range(pos_y + 1, y_size):
        south += 1
        if not forest[(pos_x, y)] < val:
            break
    west = 0
    for x in range(pos_x - 1, -1, -1):
        west += 1
        if not forest[(x, pos_y)] < val:
            break
    east = 0
    for x in range(pos_x + 1, x_size):
        east += 1
        if not forest[(x, pos_y)] < val:
            break
    return north * south * west * east

filename = 'input-08'
forest, x_size, y_size = parse_input(filename)

max_score = 0
for y in range(0, y_size):
    for x in range(0, x_size):
        score = calc_score(x, y, forest, x_size, y_size)
        max_score = max(max_score, score)

print(max_score)