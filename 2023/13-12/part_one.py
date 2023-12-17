def validate_mirror(lines: list[str], candidate: int):
    for offset in range(len(lines) - candidate):
        mirror_offset = -offset - 1
        if candidate + mirror_offset < 0:
            return True
        if lines[candidate + offset] != lines[candidate + mirror_offset]:
            return False
    return True

def find_mirror(lines: list[str]):
    prev_line = ''
    for idx, line in enumerate(lines):
        if line == prev_line and validate_mirror(lines, idx):
            return idx
        prev_line = line
    return -1


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