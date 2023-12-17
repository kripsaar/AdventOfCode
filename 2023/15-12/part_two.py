
def parse_input(filename: str):
    with open(filename, 'r') as file:
        return file.read().strip().split(',')

def hash_algorithm(input: str) -> int:
    current_value = 0
    for char in input:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value

def deconstruct_step(sequence_step: str):
    label = ''
    if '=' in sequence_step:
        label, focal_length = sequence_step.split('=')
        return label, '=', int(focal_length)
    return sequence_step[:-1], '-', None


def install_lenses(init_sequence: list[str]):
    boxes = {}
    for sequence_step in init_sequence:
        label, instruction, focal_length = deconstruct_step(sequence_step)
        box_nr = hash_algorithm(label)
        if box_nr not in boxes:
            boxes[box_nr] = {}
        box = boxes[box_nr]
        if instruction == '-':
            box.pop(label, None)
        else:
            box[label] = focal_length
    return boxes

def calc_focusing_power(box_nr: int, box: dict) -> int:
    box_power = 0
    for idx, focal_length in enumerate(box.values()):
        box_power += (1 + box_nr) * (idx + 1) * focal_length
    return box_power

init_sequence = parse_input('input-15')
boxes = install_lenses(init_sequence)
result = 0
for box_nr, box in boxes.items():
    result += calc_focusing_power(box_nr, box)

print(result)