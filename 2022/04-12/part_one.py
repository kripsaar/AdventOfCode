
def to_range(string: str):
    left, right = [int(item) for item in string.split('-')]
    return set(range(left, right + 1))

def parse_input(filename: str):
    overlap_count = 0
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            left, right = line.split(',')
            left_range = to_range(left)
            right_range = to_range(right)
            if left_range.issubset(right_range) or right_range.issubset(left_range):
                overlap_count += 1
    return overlap_count

filename = "input-04"
result = parse_input(filename)
print(result)