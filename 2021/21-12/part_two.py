import itertools
import collections

dice_rolls = []
dice_values = []
win_counter = {0: 0, 1: 0}
value_frequency = {}
score_dirac = {}

class State:
    def __init__(self, pos0, pos1, score0, score1):
        self.pos0 = pos0
        self.pos1 = pos1
        self.score0 = score0
        self.score1 = score1

class Score:
    def __init__(self, score_player_one: int, score_player_two: int) -> None:
        self.zero = score_player_one
        self.one = score_player_two

    def __repr__(self) -> str:
        return f"({self.zero} : {self.one})"

    def get_score(self, player: int) -> int:
        if player == 0:
            return self.zero
        else:
            return self.one

    def increment(self, player, value):
        if player == 0:
            return Score(self.zero + value, self.one)
        else:
            return Score(self.zero, self.one + value)

    def copy(self):
        return Score(self.zero, self.one)

    def __hash__(self) -> int:
        return hash((self.zero, self.one))


class Dirac:
    def __init__(self, positions, scores, previous_dice_roll, previous_player, universes: int = 1, initial = False):
        self.universes = universes
        self.positions = positions
        self.scores = scores
        self.previous_dice_roll = previous_dice_roll
        self.previous_player = previous_player
        self.initial = initial

    def step(self):
        if not self.initial:
            position = self.positions[self.previous_player]
            position = (position + self.previous_dice_roll) % 10
            score = position + 1
            self.scores = self.scores.increment(self.previous_player, score)
            self.positions[self.previous_player] = position
            if self.scores in score_dirac:
                other = score_dirac[self.scores]
                other.universes += self.universes
                return
            else:
                score_dirac[self.scores] = self
            if self.scores.get_score(self.previous_player) >= 21:
                win_counter[self.previous_player] += self.universes
                return
            next_player = (self.previous_player + 1) % 2
        else:
            next_player = 0
        for dice_sum in dice_values:
            new_game = Dirac(self.positions.copy(), self.scores.copy(), dice_sum, next_player, self.universes + value_frequency[dice_sum] - 1)
            new_game.step()

def init():
    global dice_rolls
    global value_frequency
    global dice_values
    dice_rolls = list(itertools.product(range(1,4), repeat=3))
    dice_values = [sum(roll) for roll in dice_rolls]
    value_frequency = dict(collections.Counter(dice_values))
    dice_values = list(value_frequency.keys())

def play(initial_positions: dict):
    game = Dirac(initial_positions, Score(0,0), 0, 1, 1, True)
    game.step()

def calc_answer():
    most_wins = max(win_counter.values())
    return most_wins

def parse_input(filename: str):
    positions = {}
    with open(filename, mode="r") as input:
        lines = input.readlines()
        for index, line in enumerate(lines):
            positions[index] = int(line.strip().split(": ")[1]) - 1
    return positions

init()
initial_positions = parse_input("input-21-test")
play(initial_positions)
print(win_counter)
print(f"Answer: {calc_answer()}")

# 4049420