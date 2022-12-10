from collections import deque

class CPU:
    def __init__(self, instructions):
        self.reg_x = 1
        self.cycle = 0
        self.inst_buffer = None
        self.instructions = instructions
        self.image = {}
    
    def addx(self, val: int):
        self.reg_x += val

    def draw(self):
        x = (self.cycle - 1) % 40
        y = int((self.cycle - 1) / 40)
        val = ' '
        if x in range(self.reg_x - 1, self.reg_x + 2):
            val = '█'
        self.image[(x, y)] = val

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

        self.draw()

    def run(self):
        while self.instructions or self.inst_buffer:
            self.step()

    def __repr__(self) -> str:
        y_size = int((self.cycle - 1) / 40) + 1
        x_size = 40
        res = ""
        for y in range(0, y_size):
            line = ""
            for x in range(0, x_size):
                if (x, y) in self.image:
                    line += self.image[(x, y)]
                else:
                    line += ' '
            line += '\n'
            res += line
        return res

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
print(cpu)