
last_die_roll = 0
die_roll_count = 0
positions = {}
scores = {0: 0, 1: 0}

def roll_dice():
    global last_die_roll
    global die_roll_count
    die_roll_count += 1
    last_die_roll += 1
    if last_die_roll == 101:
        last_die_roll = 1
    return last_die_roll

def step(player: int):
    global positions
    global scores
    position = positions[player]
    position = (position + roll_dice() + roll_dice() + roll_dice()) % 10
    scores[player] += position + 1
    positions[player] = position

def play():
    while True:
        for player in range(2):
            step(player)
            if scores[player] >= 1000:
                return

def calc_answer():
    losing_score = min(scores.values())
    return losing_score * die_roll_count

def parse_input(filename: str):
    global positions
    with open(filename, mode="r") as input:
        lines = input.readlines()
        for index, line in enumerate(lines):
            positions[index] = int(line.strip().split(": ")[1]) - 1
    return positions

parse_input("input-21")
play()
print(scores)
print(f"Answer: {calc_answer()}")