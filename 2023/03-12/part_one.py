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

    # for y_offset in range(-1, 2):
    #     curr_num = None
    #     for x_offset in range(-1, 2):
    #         if (x_offset, y_offset) == (0, 0):
    #             curr_num = None
    #             continue
    #         x = symbol_coords[0] + x_offset
    #         y = symbol_coords[1] + y_offset
    #         if (x, y) not in schematic:
    #             continue
    #         num = schematic[(x, y)]
    #         if num == curr_num:
    #             continue
    #         parts_numbers.append(num)
    # neighboring_nums = set()
    # for x_offset, y_offset in offsets:
    #     x = symbol_coords[0] + x_offset
    #     y = symbol_coords[1] + y_offset
    #     if (x, y) not in schematic:
    #         continue
    #     num = schematic[(x, y)]
    #     neighboring_nums.add(num)
    # parts_numbers.extend(neighboring_nums)

def parse_input(filename: str):
    schematic = {}
    numbers = []
    symbol_coords = []
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
                    symbol_coords.append((x, y))
                if curr_number_str:
                    for index in curr_number_idx:
                        schematic[index] = int(curr_number_str)
                    numbers.append((int(curr_number_str), curr_number_idx))
                    curr_number_str = ''
                    curr_number_idx = []
    return schematic, symbol_coords, numbers

schematic, symbol_coords, numbers = parse_input('input-03')
parts_numbers = list(filter(lambda num : check_neighborhood(num, symbol_coords), numbers))
result = sum([value for (value, coords) in parts_numbers])
print(result)