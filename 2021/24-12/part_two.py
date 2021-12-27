from enum import Enum
from typing import Union
from math import trunc

class Operation(Enum):
    INPUT = "inp"
    ADD = "add"
    MULTIPLY = "mul"
    DIVIDE = "div"
    MODULO = "mod"
    EQUALS = "eql"

class Instruction:
    def __init__(self, op: str, left: str, right: str = None, count: int = 0):
        self.count = count
        self.op = Operation(op)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.count} - {self.op.value} {self.left} {(self.right if self.right is not None else '')}"

class ALU:
    def __init__(self, input: list = None, w: int = 0, x: int = 0, y: int = 0, z: int = 0):
        self.input = input if input is not None else []
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"ALU: w = {self.w} x = {self.x} y = {self.y} z = {self.z}"

    def __str__(self) -> str:
        return f"ALU:\n    w = {self.w}\n    x = {self.x}\n    y = {self.y}\n    z = {self.z}"

    def read_value(self, reference: str) -> int:
        if reference is None:
            return None
        if reference.lstrip("-").isnumeric():
            return int(reference)
        elif reference == "w":
            return self.w
        elif reference == "x":
            return self.x
        elif reference == "y":
            return self.y
        elif reference == "z":
            return self.z

    def write_value(self, reference: str, value: int):
        if reference == "w":
            self.w = value
        elif reference == "x":
            self.x = value
        elif reference == "y":
            self.y = value
        elif reference == "z":
            self.z = value

    def apply_instruction(self, instruction: Instruction):
        left_value = self.read_value(instruction.left)
        right_value = self.read_value(instruction.right)
        target = instruction.left
        value = 0

        if instruction.op == Operation.INPUT:
            if not self.input:
                raise ValueError(f"Insufficient input given for program. Input instruction {instruction.count} has nothing to work with!")
            value = self.input.pop(0)

        elif instruction.op == Operation.ADD:
            value = left_value + right_value

        elif instruction.op == Operation.MULTIPLY:
            value = left_value * right_value

        elif instruction.op == Operation.DIVIDE:
            value = trunc(left_value / right_value)

        elif instruction.op == Operation.MODULO:
            value = left_value % right_value

        elif instruction.op == Operation.EQUALS:
            value = 1 if left_value == right_value else 0

        self.write_value(target, value)

def run_program(program_file_name: str, input: list):
    instructions = parse_input(program_file_name)
    alu = ALU(input)
    for instruction in instructions:
        # print()
        # print(f"Instruction: {instruction}")
        alu.apply_instruction(instruction)
        # print(alu)
    
    print(f"Final state of ALU is:")
    print(alu)

def parse_input(filename: str):
    with open(filename, mode="r") as input:
        instructions = []
        for index, line in enumerate(input.readlines()):
            instruction = Instruction(*(line.strip().split(" ")), count=(index + 1))
            instructions.append(instruction)
        return instructions

# for i in range(1, 10):
#     print()
#     print(f"Test number: 0{i}")
#     run_program("input-24-2", [0, i])
#     print()
#     print(f"Test number: 1{i}")
#     run_program("input-24-2", [1, i])
#     print()
#     print(f"Test number: 2{i}")
#     run_program("input-24-2", [2, i])


print()
print(f"Test number: 13621111481315")
run_program("input-24", [1,3,6,2,1,1,1,1,4,8,1,3,1,5])