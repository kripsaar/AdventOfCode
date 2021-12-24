import re
from typing import Tuple, Union

all_positions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (2, 1), (4, 1), (6, 1), (8, 1), (2, 2), (4, 2), (6, 2), (8, 2)]

energy_cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

class State:
    def __init__(self, positions: dict) -> None:
        self.positions = positions

    def __repr__(self) -> str:
        string = "#############\n#"
        for x in range(11):
            if (x, 0) not in self.positions:
                string += "."
            else:
                string += self.positions[(x, 0)]
        string += "#\n###"
        x = 2
        while x < 10:
            if (x, 1) not in self.positions:
                string += "."
            else:
                string += self.positions[(x, 1)]
            string += "#"
            x += 2
        string += "##\n  #"
        x = 2
        while x < 10:
            if (x, 2) not in self.positions:
                string += "."
            else:
                string += self.positions[(x, 2)]
            string += "#"
            x += 2
        string += "  \n  #########"
        return string

def path_exists(state: State, old_pos: tuple, new_pos: tuple) -> bool:
    pass

def is_move_legal(state: State, old_pos: tuple, new_pos: tuple) -> bool:
    if new_pos not in all_positions:
        # Destination position out of bounds
        return False
    
    if old_pos not in state.positions:
        # Moving nothing, illegal move
        return False

    if new_pos in state.positions:
        # Destination already occupied
        return False

    if new_pos in [(2,0), (4,0), (6,0), (8,0)]:
        # Amphipods will never stop on the space immediately outside any room.
        return False

    if new_pos[1] > 0:
        # Amphipods will never move from the hallway into a room
        if (state.positions[old_pos], new_pos[0]) not in [("A", 2), ("B", 4), ("C", 6), ("D", 8)]:
            # unless that room is their destination room 
            return False
        
        # and that room contains no amphipods which do not also have that room as their own destination
    
    # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room

    for x in range(old_pos[0], new_pos[0], 1 if old_pos[0] < new_pos[0] else -1):
        pos = (x, 0)
        if pos in state.positions:
            # Path is blocked by another amphipod
            return False
    for y in range(old_pos[1], new_pos[1], 1 if old_pos[1] < new_pos[1] else -1):
        x = old_pos[0] if old_pos[1] > 0 else new_pos[0]
        pos = (x, y)
        if pos in state.positions:
            # Path is blocked by another amphipod
            return False

    return True

def manhattan_distance(posA, posB):
    return abs(posB[0] - posA[0]) + abs(posB[1] - posA[1])

def calc_cost(state: State, old_pos: tuple, new_pos: tuple) -> int:
    distance = manhattan_distance(new_pos, old_pos)
    return distance * energy_cost[state.positions[old_pos]]


def move(state: State, old_pos: tuple, new_pos: tuple) -> Tuple[Union[int, float], State]:
    if not is_move_legal(state, old_pos, new_pos):
        return float("inf"), State(state.positions.copy)
    new_positions = state.positions.copy()
    new_positions.pop(old_pos)
    new_positions[new_pos] = state.positions[old_pos]
    new_state = State(new_positions)
    cost = calc_cost(state, old_pos, new_pos)
    return cost, new_state


def parse_input(filename: str):
    positions = {}
    with open(filename, mode="r") as input:
        lines = [line[1:-1] for line in input.readlines()[1:-1]]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if bool(re.match("[ABCD]", char)):
                    positions[(x, y)] = char
    return State(positions)

initial_state = parse_input("input-23-test")
print(initial_state)
