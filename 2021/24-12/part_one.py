from enum import Enum

class Operation(Enum):
    INPUT = "inp"
    ADD = "add"
    MULTIPLY = "mul"
    DIVIDE = "div"
    MODULO = "mod"
    EQUALS = "eql"

class Instruction:
    def __init__(self, op: str, left: str, right: str = None):
        self.op = Operation(op)
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.op.value} {self.left} {(self.right if self.right is not None else '')}"

def parse_input(filename: str):
    with open(filename, mode="r") as input:
        instructions = []
        for line in input.readlines():
            instruction = Instruction(*(line.strip().split(" ")))
            instructions.append(instruction)
        return instructions

instructions = parse_input("input-24-bin")
for instruction in instructions:
    print(instruction)