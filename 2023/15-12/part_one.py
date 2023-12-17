
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

init_sequence = parse_input('input-15')
result = sum(map(hash_algorithm, init_sequence))
print(result)