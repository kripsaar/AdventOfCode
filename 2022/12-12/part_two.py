import bisect

def parse_input(filename: str):
    start = []
    heightmap = dict()
    with open(filename, mode='r') as file:
        y = 0
        for line in file.readlines():
            line = line.strip()
            for x in range(0, len(line)):
                heightmap[(x, y)] = line[x]
                if line[x] == 'S' or line[x] == 'a':
                    start.append((x, y))
                    heightmap[(x, y)] = 'a'
            y += 1
    return heightmap, start

def evaluate(pos, prev_pos, heightmap: dict, scoremap: dict):
    if not pos in heightmap:
        return False
    if pos in scoremap and scoremap[pos] <= scoremap[prev_pos]:
        return False
    pos_height = ord(heightmap[pos])
    if heightmap[pos] == 'E':
        pos_height = ord('z')
    if pos_height > ord(heightmap[prev_pos]) + 1:
        return False
    scoremap[pos] = scoremap[prev_pos] + 1
    return True

def step(pos, heightmap: dict, scoremap: dict):
    x, y = pos
    candidates = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
    new_candidates = []
    for candidate in candidates:
        if evaluate(candidate, pos, heightmap, scoremap):
            new_candidates.append(candidate)
    return new_candidates

def run(start, heightmap: dict, scoremap: dict) -> int:
    working_set = start
    while working_set:
        current = working_set.pop()
        if heightmap[current] == 'E':
            return scoremap[current]
        candidates = step(current, heightmap, scoremap)
        for candidate in candidates:
            bisect.insort_left(working_set, candidate, key=lambda x: -scoremap[x])
        working_set = list(dict.fromkeys(working_set))
    return 0
        
def print_scoremap(heightmap: dict, scoremap: dict):
    res = ""
    for y in range(0, 100):
        if (0, y) not in heightmap:
            break
        line = ""
        for x in range(0, 100):
            if (x, y) not in heightmap:
                break
            if (x, y) in scoremap:
                line += '{:4d}'.format(scoremap[(x, y)])
            else:
                line += '    '
        line += '\n'
        res += line
    print(res)

filename = "input-12"
heightmap, start = parse_input(filename)
scoremap = dict()
for pos in start:
    scoremap[pos] = 0
score = run(start, heightmap, scoremap)

print_scoremap(heightmap, scoremap)

print(score)

