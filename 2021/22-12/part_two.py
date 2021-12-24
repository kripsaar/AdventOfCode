from enum import Enum
import itertools
import sys
import functools

turned_on = []

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

class Cuboid:
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max

    def __hash__(self) -> int:
        return hash((self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max))

    def copy(self) -> "Cuboid":
        new_cuboid = Cuboid(self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max)
        return new_cuboid

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cuboid):
            return False
        if (self.x_min == other.x_min and
            self.x_max == other.x_max and
            self.y_min == other.y_min and
            self.y_max == other.y_max and
            self.z_min == other.z_min and
            self.z_max == other.z_max):
            return True
        
        return False
            
    def intersection(self, other: "Cuboid"):
        # No intersection at all
        if (other.x_min > self.x_max or other.x_max < self.x_min or
            other.y_min > self.y_max or other.y_max < self.y_min or
            other.z_min > self.z_max or other.z_max < self.z_min ):
            return None

        # Perfect intersection
        if self == other:
            return self

        x_max = min(self.x_max, other.x_max)
        x_min = max(self.x_min, other.x_min)
        y_max = min(self.y_max, other.y_max)
        y_min = max(self.y_min, other.y_min)
        z_max = min(self.z_max, other.z_max)
        z_min = max(self.z_min, other.z_min)

        return Cuboid(x_min, x_max, y_min, y_max, z_min, z_max)
    
    def size(self):
        size = (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)
        return size

    def __sub__(self, other: "Cuboid") -> list:
        intersection = self.intersection(other)

        # no overlap
        if intersection is None:
            return [self]

        # complete overlap
        if intersection == self:
            return []
        
        results = []
        if intersection.x_min > self.x_min:
            results.append(Cuboid(self.x_min, intersection.x_min - 1, self.y_min, self.y_max, self.z_min, self.z_max))
        if intersection.y_min > self.y_min:
            results.append(Cuboid(intersection.x_min, self.x_max, self.y_min, intersection.y_min - 1, self.z_min, self.z_max))
        if intersection.z_min > self.z_min:
            results.append(Cuboid(intersection.x_min, self.x_max, intersection.y_min, self.y_max, self.z_min, intersection.z_min - 1))
        if intersection.x_max < self.x_max:
            results.append(Cuboid(intersection.x_max + 1, self.x_max, intersection.y_min, self.y_max, intersection.z_min, self.z_max))
        if intersection.y_max < self.y_max:
            results.append(Cuboid(intersection.x_min, intersection.x_max, intersection.y_max + 1, self.y_max, intersection.z_min, self.z_max))
        if intersection.z_max < self.z_max:
            results.append(Cuboid(intersection.x_min, intersection.x_max, intersection.y_min, intersection.y_max, intersection.z_max + 1, self.z_max))

        return results



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
    # instructions = simplify_instructions(instructions, -50, 50)
    return instructions

def apply(instruction: Instruction):
    print(f"Applying instruction: {instruction}")
    global turned_on
    cuboid = Cuboid(instruction.x_min, instruction.x_max, instruction.y_min, instruction.y_max, instruction.z_min, instruction.z_max)
    if instruction.command == Command.ON:
        new_turned_on = []
        for other in turned_on:
            cuboids = other - cuboid
            new_turned_on += cuboids
        new_turned_on.append(cuboid)
        turned_on = new_turned_on
    else:
        new_turned_on = []
        for other in turned_on:
            res = other - cuboid
            new_turned_on += res
        turned_on = new_turned_on
    print()
    print(f"Applied instruction: {instruction}")
    print()
    print(f"Current turned on cubes: {evaluate()}")


def run_procedure(instructions: list):
    for instruction in instructions:
        apply(instruction)

def evaluate():
    global turned_on
    lights_on = 0
    for cuboid in turned_on:
        lights_on += cuboid.size()
    return lights_on


instructions = parse_input("input-22")

run_procedure(instructions)

result = evaluate()

print(f"Turned on: {result}")