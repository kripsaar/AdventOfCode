from typing import List
from functools import cmp_to_key

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
    lists = []
    with open(filename, mode='r') as file:
        for line in file.read().replace('\n\n', '\n').splitlines():
            line = line.strip()
            lists.append(parse_list(line[1:-1]))
    return lists

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
lists = parse_input(filename)
lists.append([[2]])
lists.append([[6]])

sorted_lists = sorted(lists, key=cmp_to_key(compare))
index_div_one = sorted_lists.index([[2]]) + 1
index_div_two = sorted_lists.index([[6]]) + 1
decoder_key = index_div_one * index_div_two

print(f"[[2]] at index {index_div_one}")
print(f"[[6]] at index {index_div_two}")
print(f"Decoder key = {decoder_key}")