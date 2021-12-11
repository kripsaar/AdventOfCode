state_dict = {}
for i in range(11):
    state_dict[i] = []

octo_map = []

total_flashed = 0

map_size = 0

def parse_input(filename: str):
    global state_dict
    global octo_map
    global map_size
    with open(filename, mode="r") as input:
        lines = input.readlines()
        for y in range(len(lines)):
            line = [int(char) for char in lines[y].strip()]
            map_size += len(line)
            for x in range(len(line)):
                if len(octo_map) <= x:
                    octo_map.append([])
                octo_map[x].append(line[x])
                state_dict[line[x]].append((x, y))
    return octo_map

def print_octo_map(octo_map: list):
    x_length = len(octo_map)
    y_length = len(octo_map[0])
    for y in range(y_length):
        line = ""
        for x in range(x_length):
            line += str(octo_map[x][y])
        print(line)

def increment():
    x_length = len(octo_map)
    y_length = len(octo_map[0])
    for y in range(y_length):
        for x in range(x_length):
            octo_map[x][y] += 1
    
    for i in reversed(range(10)):
        state_dict[i + 1] = state_dict[i]

def get_neigbors(x, y):
    x_length = len(octo_map)
    y_length = len(octo_map[0])
    neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                 (x - 1, y), (x + 1, y),
                 (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    neighbors = list(filter(lambda pos: pos[0] >= 0 and pos[0] < x_length and pos[1] >= 0 and pos[1] < y_length , neighbors))
    return neighbors

def flash(x, y):
    global total_flashed
    total_flashed += 1
    
    neighbors = get_neigbors(x, y)
    for x, y in neighbors:
        value = octo_map[x][y]
        if value >= 10:
            continue
        octo_map[x][y] += 1
        state_dict[value].remove((x, y))
        state_dict[value + 1].append((x, y))


    

def step():
    increment()

    flashed = []
    while len(state_dict[10]) > 0:
        next = state_dict[10].pop(0)
        flashed.append(next)
        flash(next[0], next[1])
    state_dict[0] = flashed
    for x, y in flashed:
        octo_map[x][y] = 0

    return len(flashed) >= map_size
    

parse_input("input-11")

cur_step = 0
while True:
    cur_step += 1
    if step():
        print(f"Synchronized after {cur_step} steps!")
        break