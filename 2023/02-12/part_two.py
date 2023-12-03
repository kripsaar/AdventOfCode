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

def score_game(game_number: int, line: str):
    min_cubes = {'red':0, 'green': 0, 'blue':0}
    line = line.replace(';', ',').strip()
    for number_with_color in line.split(', '):
        num_str, color = number_with_color.split(' ')
        num = int(num_str)
        if num > min_cubes[color]:
            min_cubes[color] = num
    result = min_cubes['red'] * min_cubes['green'] * min_cubes['blue']
    # print(f'Game {game_number} power = {result}')
    return result

def read_input(filename: str):
    sum = 0
    with open(filename, 'r') as file:
        for line in file.readlines():
            start = line.find(':')
            line_number = int(line[line.find(' ') + 1:start])
            line = line[start+2:]
            sum += score_game(line_number, line)
    print(sum)

read_input("input-02")