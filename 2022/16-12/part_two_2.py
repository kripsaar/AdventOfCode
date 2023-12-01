import math
import time
from itertools import permutations, combinations

class Valve:
    def __init__(self, name: str, flow_rate: int, neighbor_names) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.distances = dict()
        self.neighbors = dict()
        for name in neighbor_names:
            self.neighbors[name] = None

    def __repr__(self) -> str:
        return self.name

    def calc_distance(self, other, path: set):
        if other.name in self.distances:
            return self.distances[other.name]
        if other.name in self.neighbors:
            self.distances[other.name] = 1
            return 1
        min_cost = math.inf
        for neighbor in self.neighbors.values():
            if neighbor.name in path:
                continue
            path_copy = path.copy()
            path_copy.add(self.name)
            cost = 1 + neighbor.calc_distance(other, path_copy)
            min_cost = min(min_cost, cost)
        return min_cost
        

    def calc_distances(self, valves):
        for valve in valves.values():
            if valve.name == self.name:
                continue
            distance = self.calc_distance(valve, set())
            self.distances[valve.name] = distance

class Volcano:
    def __init__(self, start_location, valves, remaining_minutes = 26, pressure_released = 0, release_rate = 0, elephant = False) -> None:
        self.remaining_minutes = remaining_minutes
        self.pressure_released = pressure_released
        self.release_rate = release_rate
        self.current_location = start_location
        self.closed_valves = valves.copy()
        self.elephant = elephant

    def calculate_cost(self, target_valve_name):
        return self.current_location.distances[target_valve_name] + 1

    def run(self):
        if self.remaining_minutes <= 0:
            if self.elephant:
                return self.pressure_released
            
            elephant_run = Volcano(starting_valve, self.closed_valves, 26, 0, self.release_rate, True)
            return elephant_run.run()

        max_score = self.pressure_released
        if not self.closed_valves:
            self.time_passes(self.remaining_minutes)
            return self.run()
        for valve in self.closed_valves.values():
            cost = self.calculate_cost(valve.name)
            valves_copy = self.closed_valves.copy()
            del valves_copy[valve.name]
            copy = Volcano(valve, valves_copy, self.remaining_minutes, self.pressure_released, self.release_rate)
            elapsed = min(cost, self.remaining_minutes)
            copy.time_passes(elapsed)
            copy.release_rate += valve.flow_rate
            score = copy.run()
            max_score = max(max_score, score)
        return max_score

    def time_passes(self, minutes: int):
        self.remaining_minutes -= 1 * minutes
        self.pressure_released += self.release_rate * minutes
        print(f"{minutes} passed. {self.remaining_minutes} minutes remain.")
        print(f"Released total of {self.pressure_released} at current rate of {self.release_rate}")
        print(f"Remaining valves: {self.closed_valves}")

def parse_input(filename: str) -> dict:
    valves = dict()
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            line = line.strip()
            name = line[6:8]
            flow_rate = int(line[line.find('rate=') + 5:line.find('; ')])
            neighbors = line[line.rfind('valve') + 5:].lstrip('s').strip().split(', ')
            valve = Valve(name, flow_rate, neighbors)
            valve.distances[name] = 0
            valves[name] = valve
        
        for valve in valves.values():
            for neighbor_name in valve.neighbors.keys():
                valve.neighbors[neighbor_name] = valves[neighbor_name]
                valve.distances[neighbor_name] = 1
    
    return valves

def purge_empty_valves(valves):
    copy = valves.copy()
    for valve in copy.values():
        if valve.flow_rate == 0:
            del valves[valve.name]

def calc_cost(source: Valve, target: Valve):
    return source.distances[target.name] + 1

def calc_run_cost(run: list[Valve]):
    cost = calc_cost(starting_valve, run[0])
    for i in range(0, len(run) - 1):
        cost += calc_cost(run[i], run[i + 1])
    return cost

def calc_run_value(run: list[Valve], max_time: int):
    remaining = max_time
    prev = starting_valve
    score = 0
    for curr in run:
        remaining -= calc_cost(prev, curr)
        score += curr.flow_rate * remaining
        prev = curr
    return score

class Run:
    def __init__(self, valves, unused_valves, cost = 0, value = 0) -> None:
        self.valves = valves
        self.cost = cost
        self.value = value
        self.unused_valves = unused_valves

    def __repr__(self) -> str:
        return f"{self.valves} === cost: {self.cost} === value: {self.value}"

def run(prev_run: Run, best_value = 0):
    if not prev_run.unused_valves:
        return []

    new_runs = []
    last_valve = prev_run.valves[-1]
    for valve in prev_run.unused_valves:
        new_valves = prev_run.valves.copy()
        new_valves.append(valve)
        new_cost = prev_run.cost + calc_cost(last_valve, valve)
        if new_cost >= max_time:
            continue
        new_value = prev_run.value + ((max_time - new_cost) * valve.flow_rate)
        new_unused_valves = prev_run.unused_valves.copy()
        new_unused_valves.remove(valve)
        new_run = Run(new_valves, new_unused_valves, new_cost, new_value)
        if new_value >= best_value:
            new_runs.append(new_run)
        new_runs.extend(run(new_run, best_value))
    return new_runs

filename = 'input-16'
valves = parse_input(filename)
max_time = 26

for valve in valves.values():
    valve.calc_distances(valves)

starting_valve = valves['AA']

purge_empty_valves(valves)
print(f"Non-zero valve count: {len(valves)}")

possible_runs = []
unused_valves = list(valves.values()).copy()

all_runs = run(Run([starting_valve], unused_valves))
sorted_runs = sorted(all_runs, reverse=True, key=lambda x: x.value)[0:4000]
best_value = sorted_runs[0].value

print(f"Found {len(sorted_runs)} runs")

candidates = []
total_combinations = combinations(sorted_runs, 2)
# print(f"Total combinations: {len(list(total_combinations))}")
for left, right in total_combinations:
    if not set(left.valves[1:]).isdisjoint(set(right.valves[1:])):
        # print(f"left: {left.valves[1:]}, right: {right.valves[1:]}")
        continue
    # if left.cost + right.cost > max_time * 2:
    #     continue
    if left.value + right.value < best_value:
        continue

    best_value = left.value + right.value

    combined_run = Run(left.valves[1:] + right.valves[1:], [], left.cost + right.cost, left.value + right.value)
    candidates.append(combined_run)

print(f"Found {len(candidates)} candidates")

final_result = max(candidates, key=lambda x: x.value)
print(f"Final result: {final_result}")

# expanded_runs = []
# for single_run in all_runs:
#     starting_valves = single_run.valves.copy()
#     starting_valves.append(starting_valve)
#     new_run = Run(starting_valves, single_run.unused_valves.copy(), 0, single_run.value)
#     expanded_runs.extend(run(new_run, best_value))

# final_result = max(expanded_runs, key=lambda x: x.value)
# print(f"Final result: {final_result}")