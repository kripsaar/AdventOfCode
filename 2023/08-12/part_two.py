from collections import deque
from math import lcm

state_map = {}
state_map_reverse = {}
solution_map = {}

def parse_input(filename: str):
    instructions = deque()
    nodes = {}
    starting_nodes = []
    with open(filename, 'r') as file:
        instructions = deque(file.readline().strip())
        
        file.readline()

        for line in file.readlines():
            node_name, node_instruction_str = line.strip().split(' = ')
            left, right = node_instruction_str.strip('()').split(', ')
            nodes[node_name] = (left, right)
            if 'A' in node_name:
                starting_nodes.append(node_name)
                state_map[node_name] = node_name
                solution_map[node_name] = []
    return instructions, nodes, starting_nodes

def check_if_finished(node: str, step_count: int):
    print(f'Checking {step_count} for {node}')
    print(f'(current solutions = {solution_map[node]})')
    for solution in solution_map[node]:
        if step_count % solution == 0:
            return True
    return False


def traverse(instructions: deque[str], nodes: dict[str, tuple[str, str]], starting_nodes: list[str]):
    step_count = 0
    unfinished = starting_nodes.copy()
    while unfinished:
        step_count += 1
        instruction = instructions.popleft()
        instructions.append(instruction)
        idx = 0
        if instruction == 'L':
            idx = 0
        else:
            idx = 1
        still_unfinished = unfinished.copy()
        for starting_node in still_unfinished:
            node = state_map[starting_node]
            next_node = nodes[node][idx]
            state_map[starting_node] = next_node
            if 'Z' in next_node:
                finished = check_if_finished(starting_node, step_count)
                if finished:
                    unfinished.remove(starting_node)
                else:
                    solution_map[starting_node].append(step_count)
    return step_count

instructions, nodes, starting_nodes = parse_input('input-08')
print(starting_nodes)
step_count = traverse(instructions, nodes, starting_nodes)

all_solutions = []
for solutions in solution_map.values():
    all_solutions.extend(solutions)

all_unique_solutions = set(all_solutions)

result = lcm(*all_unique_solutions)
print(result)