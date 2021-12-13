
def parse_input(filename: str):
    with open(filename, mode="r") as input:
        paper = []
        input = input.read().split("\n\n")
        
        instructions = []
        instructions_prelim = [item.strip() for item in input[1].split("\n")]
        for instruction in instructions_prelim:
            instruction = instruction[(instruction.rfind("=") - 1):]
            axis, line = instruction.split("=")
            instructions.append((axis, int(line)))

        lines = [line.strip() for line in input[0].split("\n")]
        for line in lines:
            x, y = [int(coord) for coord in line.split(",")]
            paper.append((x, y))
        
        return set(paper), instructions

def print_paper(paper):
    max_x = 0
    max_y = 0
    for point in paper:
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if (x, y) in paper:
                line += "#"
            else:
                line += " "
        print(line)

def fold(paper: set, instruction: tuple):
    to_fold = set()
    if instruction[0] == "x":
        to_fold = set(filter(lambda point: point[0] > instruction[1], paper))
    if instruction[0] == "y":
        to_fold = set(filter(lambda point: point[1] > instruction[1], paper))
    folded_paper = paper - to_fold
    for coord in to_fold:
        if instruction[0] == "x":
            folded_paper.add((fold_point(coord[0], instruction[1]), coord[1]))
        if instruction[0] == "y":
            folded_paper.add((coord[0], fold_point(coord[1], instruction[1])))
    return folded_paper


def fold_point(point, fold_line):
    return (-(point - fold_line)) % fold_line

paper, instructions = parse_input("input-13")

for instruction in instructions:
    paper = fold(paper, instruction)

print_paper(paper)