import re
from typing import Tuple, Union
from functools import cache
import itertools
import bisect


all_positions = [(0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (10, 0), (2, 1), (4, 1), (6, 1), (8, 1), (2, 2), (4, 2), (6, 2), (8, 2), (2, 3), (4, 3), (6, 3), (8, 3), (2, 4), (4, 4), (6, 4), (8, 4)]

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
        string += "  \n  #"
        x = 2
        while x < 10:
            if (x, 3) not in self.positions:
                string += "."
            else:
                string += self.positions[(x, 3)]
            string += "#"
            x += 2
        string += "  \n  #"
        x = 2
        while x < 10:
            if (x, 4) not in self.positions:
                string += "."
            else:
                string += self.positions[(x, 4)]
            string += "#"
            x += 2
        string += "  \n  #########"
        return string

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, State):
            return False
        return self.positions == o.positions

    def __hash__(self) -> int:
        return hash(frozenset(self.positions.items()))

final_state = State({(2,1) : "A", (2,2) : "A", (2,3) : "A", (2,4) : "A", (4,1) : "B", (4,2) : "B", (4,3) : "B", (4,4) : "B",  (6,1) : "C", (6,2) : "C", (6,3) : "C", (6,4) : "C", (8,1) : "D", (8,2) : "D", (8,3) : "D", (8,4) : "D"})

@cache
def path_exists(state: State, old_pos: tuple, new_pos: tuple) -> bool:
    for y in range(0, old_pos[1], 1):
        x = old_pos[0]
        pos = (x, y)
        if pos in state.positions:
            # Path is blocked by another amphipod
            return False
    for x in range(new_pos[0], old_pos[0], -1 if old_pos[0] < new_pos[0] else 1):
        pos = (x, 0)
        if pos in state.positions:
            # Path is blocked by another amphipod
            return False
    for y in range(0, new_pos[1], 1):
        x = new_pos[0]
        pos = (x, y)
        if pos in state.positions:
            # Path is blocked by another amphipod
            return False

    return True

@cache
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
        x = new_pos[0]
        for y in range(1, 5):
            if (x, y) in state.positions and state.positions[(x, y)] != state.positions[old_pos]:
                return False
    
    # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room
    if old_pos[1] == 0 and new_pos[1] == 0:
        return False

    # Amphipod in right room will not want to leave room
    if old_pos[1] > 0:
        x = old_pos[0]
        parked = False
        if ((x == 2 and state.positions[old_pos] == "A") or
            (x == 4 and state.positions[old_pos] == "B") or
            (x == 6 and state.positions[old_pos] == "C") or
            (x == 8 and state.positions[old_pos] == "D")):
            parked = True
            for y in range(old_pos[1] + 1, 5):
                if not ((x,y) in state.positions and state.positions[(x,y)] == state.positions[old_pos]):
                    parked = False
        if parked:
            return False

    # There is a better position in a room available
    if new_pos[1] > 0:
        x = new_pos[0]
        for y in range(new_pos[1] + 1, 5):
            if (x, y) not in state.positions:
                return False

    if not path_exists(state, old_pos, new_pos):
        return False

    return True

def manhattan_distance(posA, posB):
    return abs(posB[0] - posA[0]) + abs(posB[1] - posA[1])

def calc_cost(state: State, old_pos: tuple, new_pos: tuple) -> int:
    distance = 0
    if old_pos[1] == 0 or new_pos == 0:
        distance = manhattan_distance(new_pos, old_pos)
    else:
        distance = old_pos[1] + new_pos[1] + (abs(new_pos[0] - old_pos[0]))
    return distance * energy_cost[state.positions[old_pos]]


def do_move(state: State, old_pos: tuple, new_pos: tuple) -> Tuple[Union[int, float], State]:
    if not is_move_legal(state, old_pos, new_pos):
        return float("inf"), State(state.positions.copy())
    new_positions = state.positions.copy()
    new_positions.pop(old_pos)
    new_positions[new_pos] = state.positions[old_pos]
    new_state = State(new_positions)
    cost = calc_cost(state, old_pos, new_pos)
    return cost, new_state

def find_moves(state: State) -> list:
    current_positions = list(state.positions.keys())
    possible_moves = itertools.product(current_positions, all_positions)
    possible_moves = list(filter(lambda move: is_move_legal(state, move[0], move[1]), possible_moves))
    return possible_moves

def score_state(state: State) -> int:
    score = 0
    for pos in state.positions.keys():
        dest = (0,0)
        if state.positions[pos] == "A":
            dest = (2,4)
        if state.positions[pos] == "B":
            dest = (4,4)
        if state.positions[pos] == "C":
            dest = (6,4)
        if state.positions[pos] == "D":
            dest = (8,4)
        score += min(calc_cost(state, pos, dest), calc_cost(state, pos, (dest[0], dest[1] - 1)), calc_cost(state, pos, (dest[0], dest[1] - 2)), calc_cost(state, pos, (dest[0], dest[1] - 3)))
    return score

def init_part_two(state: State) -> State:
    new_pos = state.positions.copy()
    for x, y in state.positions.keys():
        if y == 2:
            pos = new_pos.pop((x,y))
            new_pos[(x, 4)] = pos
    new_pos[(2, 2)] = "D"
    new_pos[(2, 3)] = "D"
    new_pos[(4, 2)] = "C"
    new_pos[(4, 3)] = "B"
    new_pos[(6, 2)] = "B"
    new_pos[(6, 3)] = "A"
    new_pos[(8, 2)] = "A"
    new_pos[(8, 3)] = "C"

    return State(new_pos)

def parse_input(filename: str):
    positions = {}
    with open(filename, mode="r") as input:
        lines = [line[1:-1] for line in input.readlines()[1:-1]]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if bool(re.match("[ABCD]", char)):
                    positions[(x, y)] = char
    return init_part_two(State(positions))

def sort(state: State):
    available_moves = [(0, state)]
    visited_states = []
    score = {}
    counter = 0
    while len(available_moves) > 0:
        counter += 1
        cost, state = available_moves.pop(0)
        
        print(f"Visited {counter} states")
        # print()
        # print(state)
        # print()

        # Final state reached -> terminate
        if state == final_state:
            return cost, state
        
        possible_moves = find_moves(state)
        for old_pos, new_pos in possible_moves:
            add_cost, next_state = do_move(state, old_pos, new_pos)
            if next_state in visited_states:
                continue
            visited_states.append(next_state)
            bisect.insort(available_moves, (cost + add_cost, next_state), key=(lambda item: item[0]))

def sort_with_heuristic(state: State):
    available_moves = [state]
    visited_states = []
    costs = {state: 0}
    scores = {state: 0}
    counter = 0
    while len(available_moves) > 0:
        counter += 1
        state = available_moves.pop(0)
        
        # print(f"Visited {counter} states")
        # print()
        # print(state)
        # print()

        # Final state reached -> terminate
        if state == final_state:
            print(f"Visited {counter} states")
            return costs[state], state
        
        possible_moves = find_moves(state)
        for old_pos, new_pos in possible_moves:
            add_cost, next_state = do_move(state, old_pos, new_pos)
            alt = costs[state] + add_cost
            if next_state not in costs:
                costs[next_state] = float("inf")
            if alt < costs[next_state]:
                costs[next_state] = alt
                score = alt + score_state(next_state)
                scores[next_state] = score
                if next_state not in available_moves:
                    bisect.insort(available_moves, next_state, key=(lambda item: scores[item]))

@cache
def sort_dfs(state: State):
    if state == final_state:
        return 0
    possible_moves = find_moves(state)
    total_cost = float("inf")
    for move in possible_moves:
        cost, new_state = do_move(state, move[0], move[1])
        cost += sort_dfs(new_state)
        total_cost = min(total_cost, cost)
    return total_cost

initial_state = parse_input("input-23")
print(initial_state)

# cost, state = sort(initial_state)
cost = sort_dfs(initial_state)

print(f"Cost: {cost}")
# print("State:")
# print()
# print(state)

# cost, state = do_move(initial_state, (6, 1), (3, 0))
# print(f"Cost: {cost}")
# print("State:")
# print()
# print(state)
# cost, state = do_move(state, (4, 1), (6, 1))
# print(f"Cost: {cost}")
# print("State:")
# print()
# print(state)