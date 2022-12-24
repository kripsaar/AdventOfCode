from __future__ import annotations
import re
import math

class Path:
    def __init__(self, board: dict[tuple[int, int], str], x_ranges: dict[int, range], y_ranges: dict[int, range], instructions: str) -> None:
        self.board = board
        self.x_ranges = x_ranges
        self.y_ranges = y_ranges
        self.instructions = instructions
        self.pos = (x_ranges[0].start, 0)
        self.direction = 'R'

    def rotate(self, direction: str):
        if direction == 'R':
            if self.direction == 'U':
                self.direction = 'R'
            elif self.direction == 'R':
                self.direction = 'D'
            elif self.direction == 'D':
                self.direction = 'L'
            elif self.direction == 'L':
                self.direction = 'U'
        else:
            if self.direction == 'U':
                self.direction = 'L'
            elif self.direction == 'L':
                self.direction = 'D'
            elif self.direction == 'D':
                self.direction = 'R'
            elif self.direction == 'R':
                self.direction = 'U'

    def get_linear_path_x(self, start, destination, wrap_arounds: int):
        wrap_arounds = min(wrap_arounds, 2)
        y = destination[1]
        step = 1
        if self.direction == 'R':
            step = 1
        else:
            step = -1
        x = start[0]
        while x != destination[0] or wrap_arounds > 0:
            prev_x = x
            x += step
            if x > self.x_ranges[y].stop - 1:
                x = x - self.x_ranges[y].stop + self.x_ranges[y].start
                wrap_arounds -= 1
            if x < self.x_ranges[y].start:
                x = x + self.x_ranges[y].stop - self.x_ranges[y].start
                wrap_arounds -= 1
            # print(f"Testing ({x},{y})")
            if self.board[(x, y)] == '#':
                return (prev_x, y)
        return destination

    def get_linear_path_y(self, start, destination, wrap_arounds: int):
        wrap_arounds = min(wrap_arounds, 2)
        x = destination[0]
        step = 1
        if self.direction == 'D':
            step = 1
        else:
            step = -1
        y = start[1]
        while y != destination[1] or wrap_arounds > 0:
            prev_y = y
            y += step
            if y > self.y_ranges[x].stop - 1:
                y = y - self.y_ranges[x].stop + self.y_ranges[x].start
                wrap_arounds -= 1
            if y < self.y_ranges[x].start:
                y = y + self.y_ranges[x].stop - self.y_ranges[x].start
                wrap_arounds -= 1
            # print(f"Testing ({x},{y})")
            if self.board[(x, y)] == '#':
                return (x, prev_y)
        return destination

    def move(self, instruction: str):
        print(f"Moving according to instruction [{instruction}]")
        x, y = self.pos
        if 'R' in instruction or 'L' in instruction:
            self.rotate(instruction[:1])
            instruction = instruction[1:]
        if self.direction == 'U' or self.direction == 'D':
            modulo = len(y_ranges[x])
            delta = int(instruction)
            if self.direction == 'U':
                delta = -delta
            dest = (y + delta - y_ranges[x].start) % modulo + y_ranges[x].start
            wrap_arounds = abs(math.floor((y + delta - y_ranges[x].start) / modulo))
            dest_pos = self.get_linear_path_y(self.pos, (x, dest), wrap_arounds)
            self.pos = dest_pos
        else:
            modulo = len(x_ranges[y])
            delta = int(instruction)
            if self.direction == 'L':
                delta = -delta
            dest = (x + delta - x_ranges[y].start) % modulo + x_ranges[y].start
            wrap_arounds = abs(math.floor((x + delta - x_ranges[y].start) / modulo))
            dest_pos = self.get_linear_path_x(self.pos, (dest, y), wrap_arounds)
            self.pos = dest_pos
        print(f"Moved from ({x}, {y}) to {self.pos}")

    def run(self):
        for instruction in instructions:
            self.move(instruction)

    def evaluate(self):
        x, y = map(lambda a: a + 1, self.pos)
        dir: int
        if self.direction == 'R':
            dir = 0
        elif self.direction == 'D':
            dir = 1
        elif self.direction == 'L':
            dir = 2
        else:
            dir = 3
        score = (1000 * y) + (4 * x) + dir 
        return score

def parse_input(filename: str):
    board = dict()
    x_ranges = dict()
    y_ranges = dict()
    instructions = []
    with open(filename, mode = 'r') as file:
        board_string, instruction_string = file.read().split('\n\n')
        y = 0
        for line in board_string.splitlines():
            line = line.strip('\n')
            line_len = len(line)
            x_start = line_len
            x_end = 0
            for x in range(0, line_len):
                char = line[x]
                if char == ' ':
                    continue
                board[(x, y)] = char
                x_start = min(x_start, x)
                x_end = max(x_end, x)
                
                if x not in y_ranges:
                    y_ranges[x] = range(y, y + 1)
                else:
                    y_ranges[x] = range(min(y_ranges[x].start, y), max(y_ranges[x].stop, y + 1))
            x_ranges[y] = range(x_start, x_end + 1)
            y += 1
        
        instructions = re.findall("[LR]{0,1}\d+", instruction_string)

    return board, x_ranges, y_ranges, instructions

filename = 'input-22'
board, x_ranges, y_ranges, instructions = parse_input(filename)
path = Path(board, x_ranges, y_ranges, instructions)

path.run()
print(path.evaluate())

# Note to self: solution coordinates start with 1 and not 0!!!