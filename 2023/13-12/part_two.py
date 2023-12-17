def validate_mirror(lines: list[str], candidate: int):
    cumulative_distance = 0
    for offset in range(len(lines) - candidate):
        mirror_offset = -offset - 1
        if candidate + mirror_offset < 0:
            break
        cumulative_distance += calc_distance(lines[candidate + offset], lines[candidate + mirror_offset])
        if cumulative_distance > 1:
            return False
    return cumulative_distance == 1

def find_mirror(lines: list[str]):
    prev_line = ''
    for idx, line in enumerate(lines):
        if calc_distance(prev_line, line) < 2 and validate_mirror(lines, idx):
            return idx
        prev_line = line
    return -1

def calc_distance(l_line: str, r_line: str) -> int:
    if len(l_line) != len(r_line):
        return abs(len(l_line) - len(r_line))
    return sum(l_char != r_char for l_char, r_char in zip(l_line, r_line))

def parse_input(filename: str):
    pattern_rows_and_columns = []
    with open(filename, 'r') as file:
        for pattern in file.read().split('\n\n'):
            rows = pattern.splitlines()
            columns = []
            for row in rows:
                for idx, char in enumerate(row):
                    if idx + 1 > len(columns):
                        columns.append(char)
                    else:
                        columns[idx] += char
            pattern_rows_and_columns.append((rows, columns))
    return pattern_rows_and_columns
    
pattern_rows_and_columns = parse_input('input-13')
result = 0
for rows, columns in pattern_rows_and_columns:
    mirror_row = find_mirror(rows)
    mirror_column = find_mirror(columns)
    if mirror_row > 0:
        result += 100 * mirror_row
    if mirror_column > 0:
        result += mirror_column

print(result)