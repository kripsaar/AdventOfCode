from collections import deque

def read_stack(line: str, stacks: dict):
    size = len(line)
    ptr = 0
    while ptr < size:
        if line[ptr] == ' ':
            ptr += 4
            continue
        pos = int(ptr / 4 + 1)
        if pos not in stacks:
            stacks[pos] = []
        stacks[pos].insert(0, line[ptr + 1])
        ptr += 4
    return stacks

def read_instruction(line: str, instructions: list):
    line = line.strip()
    line_split = line.split(' ')
    instruction = {'count': int(line_split[1]), 'from': int(line_split[3]), 'to': int(line_split[5])}
    instructions.append(instruction)
    return instructions

def parse_input(filename: str):
    stacks = {}
    instructions = []
    reading_inst = False
    with open(filename, mode='r') as file:
        for line in file.readlines():
            if line == '\n':
                reading_inst = True
                continue
            if reading_inst:
                read_instruction(line, instructions)
            else:
                read_stack(line, stacks)
    return stacks, instructions

def execute(stacks: dict, instruction: dict):
    count = instruction['count']
    remainder = stacks[instruction['from']][:-count]
    to_move = stacks[instruction['from']][-count:]
    stacks[instruction['from']] = remainder
    stacks[instruction['to']].extend(to_move)
    return stacks
    
def print_top_of_stack(stacks: dict):
    size = len(stacks)
    ptr = 0
    res = ""
    while ptr < size:
        res = res + str(stacks[ptr + 1].pop())
        ptr += 1
    print(res)

filename = 'input-05'
stacks, instructions = parse_input(filename)
while instructions:
    instruction = instructions.pop(0)
    stacks = execute(stacks, instruction)
print_top_of_stack(stacks)
