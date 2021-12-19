target_x = []
target_y = []

def find_all_possible_initial_x():
    # x = f(n) / n + (n + 1) / 2
    # f(n) = nx - (n)(n + 1) / 2
    max_x = max(target_x)
    result = []
    initial_v = 0
    while initial_v <= max_x :
        current_pos = 0
        v = initial_v
        n = 0
        while v > 0:
            current_pos, v = x_step(current_pos, v)
            n += 1
            if current_pos in target_x:
                result.append((initial_v, n))
            elif current_pos > max_x:
                result
                break
        initial_v += 1
    return result

def find_y():
    min_y = min(target_y)
    y = 0 - min_y - 1
    return y

def find_highest_y(initial_y):
    return (initial_y * initial_y + initial_y) // 2

def x_step(current_pos: int, current_v: int):
    pos = current_pos + current_v
    v = current_v - 1
    return pos, v

def parse_input(filename: str):
    global target_x
    global target_y
    with open(filename, mode="r") as input:
        line = input.readline().strip().split(": ")[1]
        values = [value[2:] for value in line.split(", ")]
        x_values = [int(value) for value in values[0].split("..")]
        y_values = [int(value) for value in values[1].split("..")]
        target_x = list(range(x_values[0], x_values[1] + 1))
        target_y = list(range(y_values[0], y_values[1] + 1))

parse_input("input-17")
# possible_x = find_all_possible_initial_x()
# print(possible_x)

initial_y = find_y()
highest_y = find_highest_y(initial_y)
print(f"Initial y: {initial_y}")
print(f"Highest y: {highest_y}")