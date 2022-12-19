import math
import time

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
    def __init__(self, start_location, valves, remaining_minutes = 30, pressure_released = 0, release_rate = 0) -> None:
        self.remaining_minutes = remaining_minutes
        self.pressure_released = pressure_released
        self.release_rate = release_rate
        self.current_location = start_location
        self.closed_valves = valves.copy()

    def calculate_score(self, target_valve_name):
        cost = self.calculate_cost(target_valve_name)
        return self.closed_valves[target_valve_name].flow_rate * (self.remaining_minutes - cost)

    def calculate_cost(self, target_valve_name):
        return self.current_location.distances[target_valve_name] + 1

    def step(self):
        print(f"Remaining minutes: {self.remaining_minutes}")
        valve_list = self.closed_valves.values()
        candidates = sorted([(self.calculate_score(valve.name), valve) for valve in valve_list], key=lambda x: x[0], reverse=True)
        print(candidates)
        score, candidate = candidates.pop(0)
        if score == 0:
            self.time_passes(self.remaining_minutes)
            return
        
        cost = self.calculate_cost(candidate.name)
        del self.closed_valves[candidate.name]
        self.current_location = candidate
        self.time_passes(cost)
        self.release_rate += candidate.flow_rate

    def step2(self):
        if self.remaining_minutes <= 0:
            return self.pressure_released

        max_score = self.pressure_released
        if not self.closed_valves:
            self.time_passes(self.remaining_minutes)
            return self.pressure_released
        for valve in self.closed_valves.values():
            cost = self.calculate_cost(valve.name)
            if cost > self.remaining_minutes:
                continue
            valves_copy = self.closed_valves.copy()
            del valves_copy[valve.name]
            copy = Volcano(valve, valves_copy, self.remaining_minutes, self.pressure_released, self.release_rate)
            copy.time_passes(cost)
            copy.release_rate += valve.flow_rate
            score = copy.step2()
            max_score = max(max_score, score)
        self.time_passes(self.remaining_minutes)
        max_score = max(self.pressure_released, max_score)
        return max_score

    def time_passes(self, minutes: int):
        self.remaining_minutes -= 1 * minutes
        self.pressure_released += self.release_rate * minutes

    def run(self):
        while self.remaining_minutes > 0:
            self.step()

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

volcano = Volcano(starting_valve, valves)
# volcano.run()
start = time.time()
print(f"Actual: {volcano.step2()}")
# print(f"Expected: {1651}")
end = time.time()
print(f"Runtime: {int(((end - start) * 1000))}ms")
# print(volcano.pressure_released)
