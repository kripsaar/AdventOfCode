bag_config = {'red':12, 'green': 13, 'blue':14}

def check_color(number_with_color: str) -> bool:
    number_with_color = number_with_color.strip()
    number_and_color = number_with_color.split(' ')
    num_str, color = number_and_color
    num = int(num_str)
    return num <= bag_config[color]

def check_set(set: str):
    for number_with_color in set.split(', '):
        if not check_color(number_with_color):
            return False
    return True

def check_line(line: str) -> bool:
    for set in line.split('; '):
        if not check_set(set):
            return False
    return True

def read_input(filename: str):
    sum = 0
    with open(filename, 'r') as file:
        for line in file.readlines():
            start = line.find(':')
            line_number = int(line[line.find(' ') + 1:start])
            line = line[start+2:]
            if not check_line(line):
                print(f"Line {line_number} is invalid.")
                continue
            sum += line_number
    print(sum)

read_input("input-02")