import math
import itertools
from intcode import *

initialProgram = []
amplifiers = []

def initAmplifiers(phases):
    global amplifiers
    amplifiers = []
    for phase in phases:
        ampComputer = IntcodeComputer(initialProgram)
        ampComputer.inputs.append(phase)
        amplifiers.append(ampComputer)

def runAmplifier(computer, input, phase):
    computer.inputs = [phase, input]
    computer.outputs = []
    computer.resetProgram()
    working = True
    while working:
        working = computer.evaluateOpcode()
    return computer.outputs[0]

def doAmplifierRun(phases):
    initAmplifiers(phases)
    i = 0
    nextAmp = amplifiers[0]
    nextAmp.inputs.append(0)
    output = 0
    while not nextAmp.terminated:
        nextAmp.runUntilPauseOrTermination()
        output = nextAmp.outputs.pop()
        i = (i + 1) % len(phases)
        nextAmp = amplifiers[i]
        nextAmp.inputs.append(output)
    return output

def findBestPhases():
    # initPhases = list(range(0, 5))
    initPhases = list(range(5, 10))
    bestPhases = initPhases
    bestOutput = 0
    for phases in list(itertools.permutations(initPhases)):
        score = doAmplifierRun(phases)
        if score > bestOutput:
            bestOutput = score
            bestPhases = phases
    return (bestOutput, bestPhases)

# with open("example3","r") as f:
with open("input","r") as f:
    initialProgram = f.read().split(",")
initialProgram = [int(i) for i in initialProgram]

computer = IntcodeComputer(initialProgram)

print(findBestPhases())