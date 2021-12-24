from enum import Enum
import itertools

turned_on = {}

class Command(Enum):
    ON = "on"
    OFF = "off"

class Instruction:
    def __init__(self, command: str, x_min, x_max, y_min, y_max, z_min, z_max):
        self.command = Command(command)
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def get_all_points(self):
        all_x = list(range(self.x_min, self.x_max + 1))
        all_y = list(range(self.y_min, self.y_max + 1))
        all_z = list(range(self.z_min, self.z_max + 1))
        points = list(itertools.product(all_x, all_y, all_z))
        return points

    def __repr__(self) -> str:
        return f"{self.command.value} x={self.x_min}..{self.x_max},y={self.y_min}..{self.y_max},z={self.z_min}..{self.z_max}"

def simplify_instructions(instructions: list, min_val: int, max_val: int):
    new_instructions = []
    for instruction in instructions:
        if instruction.x_min > max_val or instruction.x_max < min_val:
            continue
        if instruction.y_min > max_val or instruction.y_max < min_val:
            continue
        if instruction.z_min > max_val or instruction.z_max < min_val:
            continue
        x_min = max([instruction.x_min, min_val])
        x_max = min([instruction.x_max, max_val])
        y_min = max([instruction.y_min, min_val])
        y_max = min([instruction.y_max, max_val])
        z_min = max([instruction.z_min, min_val])
        z_max = min([instruction.z_max, max_val])
        new_instruction = Instruction(instruction.command.value, x_min, x_max, y_min, y_max, z_min, z_max)
        new_instructions.append(new_instruction)
    return new_instructions

def parse_instruction(line: str):
    command, positions = line.strip().split(" ")
    x, y, z = [ [int(value) for value in axis[2:].split("..")] for axis in positions.split(",")]
    instruction = Instruction(command, x[0], x[1], y[0], y[1], z[0], z[1])
    return instruction

def parse_input(filename: str):
    instructions = []
    with open(filename, mode="r") as input:
        for line in input.readlines():
            instruction = parse_instruction(line)
            instructions.append(instruction)
    instructions = simplify_instructions(instructions, -50, 50)
    return instructions

def apply(instruction: Instruction):
    global turned_on
    for point in instruction.get_all_points():
        if instruction.command == Command.ON:
            turned_on[point] = True
        else:
            if point in turned_on:
                turned_on.pop(point)

def run_procedure(instructions: list):
    for instruction in instructions:
        apply(instruction)

instructions = parse_input("input-22")

run_procedure(instructions)

print(f"Turned on: {len(turned_on.keys())}")