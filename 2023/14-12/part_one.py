
x_length = 0
y_length = 0

def parse_input(filename: str) -> dict[tuple[int, int], str]:
    global x_length
    global y_length
    rocks = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        y_length = len(lines)
        x_length = len(lines[0])
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == "O" or char == '#':
                    rocks[(x, y)] = char
    return rocks

def print_rocks(rocks: dict[tuple[int, int], str]):
    for y in range(y_length):
        line = ''
        for x in range(x_length):
            if (x, y) not in rocks:
                line += '.'
            else:
                line += rocks[(x, y)]
        print(line)

def tilt_north(rocks: dict[tuple[int, int], str]) -> dict[tuple[int, int], str]:
    tilted_rocks = {}
    for y in range(y_length):
        for x in range(x_length):
            if (x, y) not in rocks:
                continue
            if rocks[(x, y)] == '#':
                tilted_rocks[(x, y)] = rocks[(x, y)]
                continue
            target_y = y
            while target_y >= 0:
                if (x, target_y - 1) in tilted_rocks or target_y - 1 < 0:
                    break
                else:
                    target_y -= 1
            tilted_rocks[(x, target_y)] = rocks[(x, y)]
    return tilted_rocks

def score_rocks(rocks: dict[tuple[int, int], str]) -> int:
    score = 0
    for y in range(y_length):
        for x in range(x_length):
            if (x, y) not in rocks or rocks[(x, y)] == '#':
                continue
            score += y_length - y
    return score

                
rocks = parse_input('input-14')
tilted_rocks = tilt_north(rocks)
score = score_rocks(tilted_rocks)
print(score)