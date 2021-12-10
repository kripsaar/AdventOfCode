import math

currPos = 0
program = []
input = 0
outputs = []

def resolveArgs(opcode, numArgs):
    args = []
    for i in range(0, numArgs):
        if (len(opcode) > i and opcode[i] == 1):
            args.append(program[currPos + i + 1])
        else:
            args.append(program[program[currPos + i + 1]])
    return args


def addOpcode(opcode):
    global currPos
    global program

    args = resolveArgs(opcode, 2)

    res = args[0] + args[1]
    program[program[currPos + 3]] = res
    currPos += 4

def multOpcode(opcode):
    global currPos
    global program

    args = resolveArgs(opcode, 2)

    res = args[0] * args[1]
    program[program[currPos + 3]] = res
    currPos += 4

def inputOpcode():
    global currPos
    global program
    global input
    program[program[currPos + 1]] = input
    currPos += 2

def outputOpcode(opcode):
    global currPos
    global program
    global outputs
    value = resolveArgs(opcode, 1)[0]
    outputs.append(value)
    currPos += 2

def jumpConditionalOpcode(opcode, condition):
    global currPos
    global program

    args = resolveArgs(opcode, 2)

    if (condition and args[0] == 0) or ((not condition) and args[0] != 0):
        currPos += 3
        return

    currPos = args[1]

def comparisonOpcode(opcode, operation):
    global currPos
    global program

    args = resolveArgs(opcode, 2)
    res = 0
    if operation(args[0], args[1]):
        res = 1

    program[program[currPos + 3]] = res
    currPos += 4


def lessThanOpcode(opcode):
    comparisonOpcode(opcode, lambda x,y: x < y)

def equalsOpcode(opcode):
    comparisonOpcode(opcode, lambda x,y: x == y)

def evaluateOpcode():
    global currPos
    global program
    operationCode = 0
    wholeOpcode = program[currPos]
    opcodeDigits = [int(n) for n in str(wholeOpcode)]
    if (len(opcodeDigits) < 3):
        operationCode = wholeOpcode
        opcodeDigits = []
    else:
        mrd = opcodeDigits[len(opcodeDigits) - 1]
        lrd = opcodeDigits[len(opcodeDigits) - 2]
        opcodeDigits = opcodeDigits[:len(opcodeDigits) - 2]
        operationCode = int(str(lrd) + str(mrd))
        opcodeDigits.reverse()
    if operationCode == 1:
        addOpcode(opcodeDigits)
    elif operationCode == 2:
        multOpcode(opcodeDigits)
    elif operationCode == 3:
        inputOpcode()
    elif operationCode == 4:
        outputOpcode(opcodeDigits)
    elif operationCode == 5:
        jumpConditionalOpcode(opcodeDigits, True)
    elif operationCode == 6:
        jumpConditionalOpcode(opcodeDigits, False)
    elif operationCode == 7:
        lessThanOpcode(opcodeDigits)
    elif operationCode == 8:
        equalsOpcode(opcodeDigits)
    elif operationCode == 99:
        return False
    return True

with open("input","r") as f:
    program = f.read().split(",")
program = [int(i) for i in program]
program = program.copy()

input = 5

working = True
while working:
    working = evaluateOpcode()

print(outputs)