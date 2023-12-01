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
        return f"Valve with name '{self.name}'"

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
    def __init__(self, location_1, location_2, valves, remaining_minutes = 26, pressure_released = 0, release_rate = 0) -> None:
        self.remaining_minutes = remaining_minutes
        self.pressure_released = pressure_released
        self.release_rate = release_rate
        self.current_location_1 = location_1
        self.distance_1 = 0
        self.current_location_2 = location_2
        self.distance_2 = 0
        self.closed_valves = valves.copy()

    def calculate_score(self, target):
        cost = self.calculate_cost(target)
        return target.flow_rate * (self.remaining_minutes - cost)

    def calculate_cost(self, source, target):
        return source.distances[target.name] + 1

    def run(self):
        if self.remaining_minutes <= 0:
            return self.pressure_released

        max_score = self.pressure_released
        if not self.closed_valves:
            elapsed = self.remaining_minutes
            if self.distance_1 == 0:
                self.release_rate += self.current_location_1.flow_rate
                if self.distance_2 > 0:
                    elapsed = min(self.remaining_minutes, self.distance_2)
            if self.distance_2 == 0:
                self.release_rate += self.current_location_2.flow_rate
                if self.distance_1 > 0:
                    elapsed = min(self.remaining_minutes, self.distance_1)
            self.time_passes(elapsed)
            return self.run()

        if self.distance_1 == 0 and self.distance_2 == 0:
            self.release_rate += self.current_location_1.flow_rate + self.current_location_2.flow_rate
            # pick 2 new destinations
            pairs = []
            if self.current_location_1 == self.current_location_2:
                pairs = combinations(self.closed_valves.values(), 2)
            else:
                pairs = permutations(self.closed_valves.values(), 2)
            for left, right in pairs:
                cost_left = self.calculate_cost(self.current_location_1, left)
                cost_right = self.calculate_cost(self.current_location_2, right)
                valves_copy = self.closed_valves.copy()
                del valves_copy[left.name]
                del valves_copy[right.name]
                copy = Volcano(left, right, valves_copy, self.remaining_minutes, self.pressure_released, self.release_rate)
                copy.distance_1 = cost_left
                copy.distance_2 = cost_right
                elapsed = min(cost_left, cost_right, copy.remaining_minutes)
                copy.time_passes(elapsed)
                score = copy.run()
                max_score = max(max_score, score)
        else:
            if self.distance_1 == 0:
                self.release_rate += self.current_location_1.flow_rate
            elif self.distance_2 == 0:
                self.release_rate += self.current_location_2.flow_rate
            for valve in self.closed_valves.values():
                distance_left = self.distance_1
                distance_right = self.distance_2
                left = self.current_location_1
                right = self.current_location_2
                if self.distance_1 == 0:
                    distance_left = self.calculate_cost(self.current_location_1, valve)
                    left = valve
                else:
                    distance_right = self.calculate_cost(self.current_location_2, valve)
                    right = valve
                valves_copy = self.closed_valves.copy()
                del valves_copy[valve.name]
                copy = Volcano(left, right, valves_copy, self.remaining_minutes, self.pressure_released, self.release_rate)
                copy.distance_1 = distance_left
                copy.distance_2 = distance_right
                elapsed = min(copy.distance_1, copy.distance_2, copy.remaining_minutes)
                copy.time_passes(elapsed)
                score = copy.run()
                max_score = max(max_score, score)
        return max_score

    def time_passes(self, minutes: int):
        self.remaining_minutes -= 1 * minutes
        self.distance_1 -= minutes
        self.distance_2 -= minutes
        self.pressure_released += self.release_rate * minutes
        # print(f"{minutes} passed. {self.remaining_minutes} minutes remain.")
        # print(f"Distance 1 now at {self.distance_1}")
        # print(f"Distance 2 now at {self.distance_2}")
        # print(f"Released total of {self.pressure_released} at current rate of {self.release_rate}")
        # print(f"Remaining valves: {self.closed_valves}")

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

filename = 'input-16'
valves = parse_input(filename)

for valve in valves.values():
    valve.calc_distances(valves)

starting_valve = valves['AA']

purge_empty_valves(valves)

volcano = Volcano(starting_valve, starting_valve, valves)
start = time.time()
print(f"Actual: {volcano.run()}")
# print(f"Expected: {1707}")
end = time.time()
print(f"Runtime: {int(((end - start) * 1000))}ms")
