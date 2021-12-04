bit_count = []
with open('input-03', mode='r') as input:
    first_line = input.readline().strip()
    for char in first_line:
        bit_count.append({ 0 : 0, 1 : 0 })
    input.seek(0)
    for line in input:
        line = line.strip()
        for index, char in enumerate(line, 0):
            bit_count[index][int(char)] += 1

gamma = ''
epsilon = ''
for column in bit_count:
    if column[0] > column[1]:
        gamma = gamma + '0'
        epsilon = epsilon + '1'
    else:
        gamma = gamma + '1'
        epsilon = epsilon + '0'

print(f"Gamma: {gamma}")
print(f"Epsilon: {epsilon}")
print(f"Product: {int(gamma, 2) * int(epsilon, 2)}")