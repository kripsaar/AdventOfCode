
def to_range(string: str):
    left, right = [int(item) for item in string.split('-')]
    return set(range(left, right + 1))

def check(left_range: set, right_range: set):
    intersection = left_range.intersection(right_range)
    return len(intersection) > 0

def parse_input(filename: str):
    overlap_count = 0
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            left, right = line.split(',')
            left_range = to_range(left)
            right_range = to_range(right)
            if check(left_range, right_range):
                overlap_count += 1
    return overlap_count

filename = "input-04"
result = parse_input(filename)
print(result)