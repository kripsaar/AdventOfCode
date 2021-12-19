import itertools

target_x = []
target_y = []

possible_x = []
n_to_x = {}
inf_x = {}
n_to_y = {}

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
                possible_x.append(initial_v)
                if n not in n_to_x:
                    n_to_x[n] = []
                n_to_x[n].append(initial_v)
                if n == initial_v:
                    inf_x[initial_v] = n
            elif current_pos > max_x:
                break
        initial_v += 1
    return result

def find_all_possible_y():
    min_y = min(target_y)
    max_y = find_highest_initial_y()
    for y in range(min_y, max_y + 1):
        pos = 0
        v = y
        n = 0
        while pos >= min_y:
            if pos in target_y:
                if n not in n_to_y:
                    n_to_y[n] = []
                n_to_y[n].append(y)
            pos, v = y_step(pos, v)
            n += 1

def y_step(current_pos, current_v):
    pos = current_pos + current_v
    v = current_v - 1
    return pos, v


def find_highest_initial_y():
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
find_all_possible_initial_x()
find_all_possible_y()
print(n_to_y)
possible_n = n_to_y.keys()

points = []
for n in possible_n:
    ys = n_to_y[n]
    xs = list(filter(lambda x: x in inf_x and inf_x[x] < n, possible_x))
    if n in n_to_x:
        xs += n_to_x[n]
    points += list(itertools.product(xs, ys))

points = set(points)
print(len(points))

# initial_y = find_highest_initial_y()
# highest_y = find_highest_y(initial_y)
# print(f"Initial y: {initial_y}")
# print(f"Highest y: {highest_y}")