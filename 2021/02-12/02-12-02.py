horizontal_position = 0
depth = 0
aim = 0
with open('input-02', mode='r') as input:
    for line in input:
        direction, value = line.split(' ')
        value = int(value)
        if direction == 'forward':
            horizontal_position += value
            depth += aim * value
        elif direction == 'up':
            aim -= value
        elif direction == 'down':
            aim += value

print(f'Horizontal position: {horizontal_position}')
print(f'Depth: {depth}')
print(f'Product: {horizontal_position * depth}')