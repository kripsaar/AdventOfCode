import math

def parse_input(filename: str):
    numbers = []
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            number = int(line.strip())
            numbers.append(number)
    return numbers

def wrap(numbers: list):
    result = numbers.copy()
    list_len = len(numbers)
    index_list = list(range(0, list_len))
    for i in range(0, list_len):
        value = numbers[i]
        old_index = index_list.index(i)
        new_index = (old_index + value ) % (list_len - 1)
        del index_list[old_index]
        del result[old_index]
        index_list.insert(new_index, i)
        result.insert(new_index, value)
    return result

def evaluate(numbers: list):
    res = []
    start = numbers.index(0)
    for i in range(1000, 3001, 1000):
        res.append(numbers[(start + i) % len(numbers)])
    return sum(res)

filename = 'input-20'
numbers = parse_input(filename)
wrapped = wrap(numbers)
result = evaluate(wrapped)

print(result)