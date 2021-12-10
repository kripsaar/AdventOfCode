import math

def calculate(program, noun, verb):
    program[1] = noun
    program[2] = verb

    currPos = 0
    currVal = program[currPos]
    while currVal != 99:
        if currVal == 1:
            program[program[currPos + 3]] = program[program[currPos + 1]] + program[program[currPos + 2]]
        elif currVal == 2:
            program[program[currPos + 3]] = program[program[currPos + 1]] * program[program[currPos + 2]]
        currPos += 4
        currVal = program[currPos]

    return program[0]

positions = []
with open("input","r") as f:
    positions = f.read().split(",")

positions = [int(i) for i in positions]

noun = 0
verb = 0
result = calculate(positions.copy(), noun, verb)
target = 19690720
while result < target and noun < 100:
    noun += 1
    result = calculate(positions.copy(), noun, verb)
noun -= 1
result = calculate(positions.copy(), noun, verb)
while result < target and verb < 100:
    verb += 1
    result = calculate(positions.copy(), noun, verb)

if (result != target):
    print ("fail!")
else:
    print(100 * noun + verb)
