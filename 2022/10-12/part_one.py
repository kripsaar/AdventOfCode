from collections import deque

class CPU:
    def __init__(self, instructions):
        self.reg_x = 1
        self.cycle = 0
        self.check_cycles = [20, 60, 100, 140, 180, 220]
        self.signal_strength = 0
        self.inst_buffer = None
        self.instructions = instructions
    
    def addx(self, val: int):
        self.reg_x += val

    def step(self):
        self.cycle += 1
        
        if self.inst_buffer:
            count, cmd, val = self.inst_buffer
            count -= 1
            if count > 0:
                self.inst_buffer = (count, cmd, val)
            else:
                self.inst_buffer = None
                self.addx(val)

        if self.instructions and not self.inst_buffer:
            cmd, val = instructions.popleft()
            if cmd == 'addx':
                self.inst_buffer = (2, cmd, val)

        if self.cycle in self.check_cycles:
            # print(f'Cycle {self.cycle}')
            # print(f'X = {self.reg_x}')
            # print(f'Signal strength = {self.cycle * self.reg_x}')
            # print()
            self.signal_strength += self.cycle * self.reg_x

    def run(self):
        while self.instructions or self.inst_buffer:
            self.step()

def parse_input(filename: str):
    instructions = deque()
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            line_split = line.split(' ')
            cmd = line_split[0]
            val = 0
            if len(line_split) > 1:
                val = int(line_split[1])
            instructions.append((cmd, val))
    return instructions

filename = 'input-10'
instructions = parse_input(filename)

cpu = CPU(instructions)
cpu.run()

print(cpu.signal_strength)