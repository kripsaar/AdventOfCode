import math

def parse_input(filename: str):
    with open(filename, mode="r") as input:
        line = input.readline()
        return [int(item) for item in line.split(",")]

def calc_cost(list, position):
    cost = 0
    for item in list:
        cost += abs(item - position)
    return cost

def step(list, min, max, min_cost, max_cost):
    if min >= max:
        return min, min_cost
    next_pos = math.floor((min + max) / 2)
    cost = calc_cost(list, next_pos)
    if min_cost <= max_cost:
        return step(list, min, next_pos, min_cost, cost)
    else:
        return step(list, next_pos, max, cost, max_cost)
    

list = parse_input("input-07")
min = min(list)
max = max(list)
cost_min = calc_cost(list, min)
cost_max = calc_cost(list, max)

final_pos, final_cost = step(list, min, max, cost_min, cost_max)
print(f"Final position: {final_pos}")
print(f"Final cost: {final_cost}")