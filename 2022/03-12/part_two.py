
def parse_input(filename: str):
    result = []
    with open(filename, mode='r') as file:
        group = []
        counter = 0
        for line in file.readlines():
            counter += 1
            group.append(set(line.strip()))
            if counter == 3:
                counter = 0
                result.append(group)
                group = []
    return result

def find_overlap(elf_one: set, elf_two: set, elf_three: set):
    return elf_one.intersection(elf_two).intersection(elf_three)

def get_priority(item: str):
    ascii_val = ord(item)
    if item.islower():
        return ascii_val - 96
    else:
        return ascii_val - 64 + 26

filename = "input-03"
groups = parse_input(filename)
overlaps = [find_overlap(elf_one, elf_two, elf_three) for (elf_one, elf_two, elf_three) in groups]
priorities = [get_priority(overlap.pop()) for overlap in overlaps]
print(sum(priorities))