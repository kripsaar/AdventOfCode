
class Rope:
    def __init__(self, length):
        self.head = (0, 0)
        self.tail = None
        length -= 1
        if length > 0:
            self.tail = Rope(length)
        self.visited = {(0, 0)}

    def step(self, direction: str):
        x, y = self.head
        if direction == 'U':
            self.move((x, y - 1))
        elif direction == 'D':
            self.move((x, y + 1))
        elif direction == 'L':
            self.move((x - 1, y))
        elif direction == 'R':
            self.move((x + 1, y))

    def move(self, new_pos):
        self.head = new_pos
        self.visited.add(new_pos)
        if not self.tail:
            return
        new_x, new_y = new_pos
        tail_x, tail_y = self.tail.head
        if abs(new_x - tail_x) >= 2 or abs(new_y - tail_y) >= 2:
            dis_x = new_x - tail_x
            dis_y = new_y - tail_y
            tail_x = tail_x + max(min(dis_x, 1), -1)
            tail_y = tail_y + max(min(dis_y, 1), -1)
            self.tail.move((tail_x, tail_y))

    def get_tail_visited(self):
        if not self.tail:
            return self.visited
        else:
            return self.tail.get_tail_visited()

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
rope = Rope(10)

for instruction in instructions:
    execute_instruction(rope, instruction)

print(len(rope.get_tail_visited()))