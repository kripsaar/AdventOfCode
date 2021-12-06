
def parse_input(filename: str):
    with open(filename, mode="r") as input:
        input = [int(item) for item in input.readline().split(",")]
        fish_map = {}
        for index in range(9):
            fish_map[index] = len(list(filter(lambda item: item == index, input)))
        return fish_map

def step(fish_map):
    next_map = {}
    for index in range(1, 9):
        next_map[index - 1] = fish_map[index]
    next_map[6] += fish_map[0]
    next_map[8] = fish_map[0]
    return next_map

def simulate(filename: str, days: int):
    fish_map = parse_input(filename)
    for day in range(days):
        fish_map = step(fish_map)
    print(f"Input: {filename}")
    print(f"Days: {days}")
    print(f"Population: {sum(fish_map.values())}")

simulate("input-06-test", 256)
simulate("input-06", 256)
