from typing import List

def parse_list(list_string: str):
    list_string = list_string.strip()
    res = []
    while list_string:
        if list_string[0] == ',':
            list_string = list_string[1:]
            continue
        if list_string[0] == '[':
            close = list_string.find(']')
            close_count = 1
            open_count = list_string[:close].count('[')
            while open_count > close_count:
                close += list_string[close + 1:].find(']') + 1
                close_count += 1
                open_count = list_string[:close].count('[')
            res.append(parse_list(list_string[1:close]))
            list_string = list_string[close + 1:]
        else:
            end = list_string.find(',')
            if end == -1:
                res.append(int(list_string))
                list_string = ""
                break
            res.append(int(list_string[:end]))
            list_string = list_string[end + 1:]
    return res

def parse_input(filename: str):
    pairs = dict()
    with open(filename, mode='r') as file:
        index = 1
        for pair_str in file.read().split('\n\n'):
            lines = pair_str.splitlines()
            left = parse_list(lines[0].strip()[1:-1])
            right = parse_list(lines[1].strip()[1:-1])
            pairs[index] = (left, right)
            index += 1
    return pairs

def compare_int(left: int, right: int):
    if left < right:
        return -1
    if left == right:
        return 0
    if left > right:
        return 1

def compare_list(left: list, right: list):
    if (not left) and (not right):
        return 0
    if (not left) and right:
        return -1
    if left and (not right):
        return 1
    
    first_result = compare(left[0], right[0])
    if first_result == 0:
        return compare_list(left[1:], right[1:])
    return first_result

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return compare_int(left, right)
    
    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    
    return compare_list(left, right)

filename = 'input-13'
pairs = parse_input(filename)

result = 0
for index, pair in pairs.items():
    left, right = pair
    pair_comparison = compare(left, right)
    if pair_comparison == -1:
        result += index

print(result)