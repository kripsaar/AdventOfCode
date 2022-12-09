
class Rope:
    def __init__(self):
        self.head = (0, 0)
        self.tail = (0, 0)
        self.tail_visited = {(0, 0)}

    def step(self, direction: str):
        if direction == 'U':
            self.step_up()
        elif direction == 'D':
            self.step_down()
        elif direction == 'L':
            self.step_left()
        elif direction == 'R':
            self.step_right()

    def step_up(self):
        head_x, head_y = self.head
        tail_x, tail_y = self.tail
        head_y -= 1
        if tail_y - head_y >= 2:
            self.tail = (head_x, head_y + 1)
            self.tail_visited.add(self.tail)
        self.head = (head_x, head_y)

    def step_down(self):
        head_x, head_y = self.head
        tail_x, tail_y = self.tail
        head_y += 1
        if head_y - tail_y >= 2:
            self.tail = (head_x, head_y - 1)
            self.tail_visited.add(self.tail)
        self.head = (head_x, head_y)

    def step_left(self):
        head_x, head_y = self.head
        tail_x, tail_y = self.tail
        head_x -= 1
        if tail_x - head_x >= 2:
            self.tail = (head_x + 1, head_y)
            self.tail_visited.add(self.tail)
        self.head = (head_x, head_y)

    def step_right(self):
        head_x, head_y = self.head
        tail_x, tail_y = self.tail
        head_x += 1
        if head_x - tail_x >= 2:
            self.tail = (head_x - 1, head_y)
            self.tail_visited.add(self.tail)
        self.head = (head_x, head_y)


def parse_input(filename:str):
    instructions = []
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            direction, distance = line.split(' ')
            instructions.append((direction, int(distance)))
    return instructions

def execute_instruction(rope: Rope, instruction):
    direction, distance = instruction
    for i in range(0, distance):
        rope.step(direction)

filename = 'input-09'
instructions = parse_input(filename)
rope = Rope()

for instruction in instructions:
    execute_instruction(rope, instruction)

print(len(rope.tail_visited))