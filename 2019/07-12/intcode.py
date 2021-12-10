import math

class IntcodeComputer:
    def __init__(self, program):
        self.initialProgram = program.copy()
        self.program = program.copy()
        self.currPos = 0
        self.inputs = []
        self.outputs = []
        self.terminated = False

    def resetProgram(self):
        self.currPos = 0
        self.program = self.initialProgram.copy()

    def resolveArgs(self, opcode, numArgs):
        args = []
        for i in range(0, numArgs):
            if (len(opcode) > i and opcode[i] == 1):
                args.append(self.program[self.currPos + i + 1])
            else:
                args.append(self.program[self.program[self.currPos + i + 1]])
        return args


    def addOpcode(self, opcode):
        args = self.resolveArgs(opcode, 2)

        res = args[0] + args[1]
        self.program[self.program[self.currPos + 3]] = res
        self.currPos += 4

    def multOpcode(self, opcode):
        args = self.resolveArgs(opcode, 2)

        res = args[0] * args[1]
        self.program[self.program[self.currPos + 3]] = res
        self.currPos += 4

    def inputOpcode(self):
        if len(self.inputs) < 1:
            return False
        input = self.inputs.pop(0)
        self.program[self.program[self.currPos + 1]] = input
        self.currPos += 2
        return True

    def outputOpcode(self, opcode):
        value = self.resolveArgs(opcode, 1)[0]
        self.outputs.append(value)
        self.currPos += 2

    def jumpConditionalOpcode(self, opcode, condition):
        args = self.resolveArgs(opcode, 2)

        if (condition and args[0] == 0) or ((not condition) and args[0] != 0):
            self.currPos += 3
            return

        self.currPos = args[1]

    def comparisonOpcode(self, opcode, operation):
        args = self.resolveArgs(opcode, 2)
        res = 0
        if operation(args[0], args[1]):
            res = 1

        self.program[self.program[self.currPos + 3]] = res
        self.currPos += 4


    def lessThanOpcode(self, opcode):
        self.comparisonOpcode(opcode, lambda x,y: x < y)

    def equalsOpcode(self, opcode):
        self.comparisonOpcode(opcode, lambda x,y: x == y)

    def evaluateOpcode(self):
        if self.terminated:
            return False
        operationCode = 0
        wholeOpcode = self.program[self.currPos]
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
            self.addOpcode(opcodeDigits)
        elif operationCode == 2:
            self.multOpcode(opcodeDigits)
        elif operationCode == 3:
            if not self.inputOpcode():
                return False
        elif operationCode == 4:
            self.outputOpcode(opcodeDigits)
        elif operationCode == 5:
            self.jumpConditionalOpcode(opcodeDigits, True)
        elif operationCode == 6:
            self.jumpConditionalOpcode(opcodeDigits, False)
        elif operationCode == 7:
            self.lessThanOpcode(opcodeDigits)
        elif operationCode == 8:
            self.equalsOpcode(opcodeDigits)
        elif operationCode == 99:
            self.terminated = True
            return False
        return True

    def runUntilPauseOrTermination(self):
        running = True
        while running:
            running = self.evaluateOpcode()