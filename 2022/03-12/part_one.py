
def parse_input(filename: str):
    result = []
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            first_half = line[:int(len(line) / 2)]
            second_half = line[int(len(line) / 2):]
            result.append((first_half, second_half))
    return result

def partition_to_set(partition: str):
    return set(partition)

def find_overlap(left_partition_set: set, right_partition_set: set):
    return left_partition_set.intersection(right_partition_set)

def get_priority(item: str):
    ascii_val = ord(item)
    if item.islower():
        return ascii_val - 96
    else:
        return ascii_val - 64 + 26

filename = "input-03"
partitions = parse_input(filename)
partition_sets = [(partition_to_set(left_partition), partition_to_set(right_partition)) for (left_partition, right_partition) in partitions]
overlaps = [find_overlap(left, right) for (left, right) in partition_sets]
priorities = [get_priority(overlap.pop()) for overlap in overlaps]
print(sum(priorities))