
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

def find_visible_set(forest, x_size: int, y_size: int):
    visible_from_left = set()
    visible_from_right = set()
    visible_from_top = set()
    visible_from_bottom = set()
    top_lim = {}
    bottom_lim = {}
    for x in range(0, x_size):
        top_lim[x] = -1
        bottom_lim[x] = -1
    for y in range(0, y_size):
        left_lim = -1
        for x in range(0, x_size):
            val = forest[(x, y)]
            if val > top_lim[x]:
                visible_from_top.add((x, y))
                top_lim[x] = val
            if val > left_lim:
                visible_from_left.add((x, y))
                left_lim = val
    for y in range(y_size - 1, -1, -1):
        right_lim = -1
        for x in range(x_size - 1, -1, -1):
            val = forest[(x, y)]
            if val > bottom_lim[x]:
                visible_from_bottom.add((x, y))
                bottom_lim[x] = val
            if val > right_lim:
                visible_from_right.add((x, y))
                right_lim = val
    return visible_from_left.union(visible_from_right).union(visible_from_top).union(visible_from_bottom)

def print_visible(visible_set, forest, x_size, y_size):
    for y in range(0, y_size):
        line = ""
        for x in range(0, x_size):
            if (x, y) in visible_set:
                line += str(forest[(x, y)])
            else:
                line += ' '
        print(line)

filename = 'input-08'
forest, x_size, y_size = parse_input(filename)

visible_set = find_visible_set(forest, x_size, y_size)
print(len(visible_set))