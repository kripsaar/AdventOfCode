
def read_input(filename: str):
    elves = []
    with open(filename, mode='r') as file:
        current_elf = 0
        for line in file.readlines():
            if line == '\n':
                elves.append(current_elf)
                current_elf = 0
                continue
            current_elf += int(line)
    return elves
            
elves = read_input('input-01')
max_calories = max(elves)
print(max_calories)