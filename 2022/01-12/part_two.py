
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
        if current_elf != 0:
            elves.append(current_elf)
    return elves
            
elves = read_input('input-01')
sorted_elves = sorted(elves, reverse=True)
top_three = sorted_elves[:3]
print(top_three)

aggregated_calories = sum(top_three)

print(aggregated_calories)