from collections import deque

def parse_input(filename: str):
    instructions = deque()
    nodes = {}
    with open(filename, 'r') as file:
        instructions = deque(file.readline().strip())
        
        file.readline()

        for line in file.readlines():
            node_name, node_instruction_str = line.strip().split(' = ')
            left, right = node_instruction_str.strip('()').split(', ')
            nodes[node_name] = (left, right)
    return instructions, nodes

def traverse(instructions: deque[str], nodes: dict[str, tuple[str, str]]):
    current_pos = 'AAA'
    step_count = 0
    while current_pos != 'ZZZ':
        instruction = instructions.popleft()
        instructions.append(instruction)
        if instruction == 'L':
            current_pos = nodes[current_pos][0]
        else:
            current_pos = nodes[current_pos][1]
        step_count += 1
    return step_count

instructions, nodes = parse_input('input-08')
step_count = traverse(instructions, nodes)
print(step_count)