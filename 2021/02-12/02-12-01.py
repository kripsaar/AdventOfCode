horizontal_position = 0
depth = 0
with open('input-02', mode='r') as input:
    for line in input:
        direction, value = line.split(' ')
        value = int(value)
        if direction == 'forward':
            horizontal_position += value
        elif direction == 'up':
            depth -= value
        elif direction == 'down':
            depth += value

print(f'Horizontal position: {horizontal_position}')
print(f'Depth: {depth}')
print(f'Product: {horizontal_position * depth}')