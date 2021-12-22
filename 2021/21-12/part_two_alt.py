import functools
import itertools
import collections

last_die_roll = 0
die_roll_count = 0
positions = {}
scores = {0: 0, 1: 0}

dice_rolls = []
dice_values = []
value_frequency = {}

def init():
    global dice_rolls
    global value_frequency
    global dice_values
    dice_rolls = list(itertools.product(range(1,4), repeat=3))
    dice_values = [sum(roll) for roll in dice_rolls]
    value_frequency = dict(collections.Counter(dice_values))
    dice_values = list(value_frequency.keys())

@functools.cache
def step(pos0, pos1, score0, score1, previous_player):
    if score0 >= 21:
        return 1, 0
    elif score1 >= 21:
        return 0, 1
    next_player = (previous_player + 1) % 2
    wins = []
    for dice_roll in dice_rolls:
        new_pos0 = pos0
        new_score0 = score0
        new_pos1 = pos1
        new_score1 = score1
        dice_value = sum(dice_roll)
        if next_player == 0:
            new_pos0 = (new_pos0 + dice_value) % 10
            new_score0 += new_pos0 + 1
        else:
            new_pos1 = (new_pos1 + dice_value) % 10
            new_score1 += new_pos1 + 1
        wins.append(step(new_pos0, new_pos1, new_score0, new_score1, next_player))
    return sum(a for a, _ in wins), sum(b for _, b in wins)
    

def play(init_positions):
    wins = step(init_positions[0], init_positions[1], 0, 0, 1)
    print(f"Player 0 won {wins[0]} times")
    print(f"Player 1 won {wins[1]} times")

    print(f"Most wins: {max(wins)}")

def parse_input(filename: str):
    global positions
    with open(filename, mode="r") as input:
        lines = input.readlines()
        for index, line in enumerate(lines):
            positions[index] = int(line.strip().split(": ")[1]) - 1
    return positions

init()
init_positions = parse_input("input-21")

play(init_positions)