offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

def check_neighborhood(num_with_coords, symbol_coords) -> bool:
    num, coords = num_with_coords
    for coord in coords:
        for x_offset, y_offset in offsets:
            x = coord[0] + x_offset
            y = coord[1] + y_offset
            if (x, y) in symbol_coords:
                return True
    return False

def get_symbol_neighbors(symbol, schematic):
    neighbors = []
    for x_offset, y_offset in offsets:
        x = symbol[1][0][0] + x_offset
        y = symbol[1][0][1] + y_offset
        if (x, y) in schematic and isinstance(schematic[(x, y)][0], int) and schematic[(x, y)] not in neighbors:
            neighbors.append(schematic[(x, y)])
    # print(f'Symbol: {symbol}\nNeighbors: {neighbors}\n')
    return neighbors

def parse_input(filename: str):
    schematic = {}
    numbers = []
    symbols = []
    with open(filename, 'r') as file:
        for y, line in enumerate(file.readlines()):
            curr_number_str = ''
            curr_number_idx = []
            for x, char in enumerate(line):
                if char.isnumeric():
                    curr_number_str += char
                    curr_number_idx.append((x, y))
                    continue
                if not char == '.' and not char == '\n':
                    schematic[(x, y)] = char
                    symbols.append((char, [(x, y)]))
                if curr_number_str:
                    for index in curr_number_idx:
                        schematic[index] = (int(curr_number_str), curr_number_idx)
                    numbers.append((int(curr_number_str), curr_number_idx))
                    curr_number_str = ''
                    curr_number_idx = []
    return schematic, symbols, numbers

schematic, symbols, numbers = parse_input('input-03')
stars = list(filter(lambda symbol : symbol[0] == '*', symbols))
star_neighbors = [get_symbol_neighbors(symbol, schematic) for symbol in symbols]
part_numbers = [list(map(lambda neighbor : neighbor[0], neighbors)) for neighbors in filter(lambda neighbors : len(neighbors) == 2, star_neighbors)]
gear_ratios = [a * b for (a, b) in part_numbers]
result = sum(gear_ratios)
print(result)