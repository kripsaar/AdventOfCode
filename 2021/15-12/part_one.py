import bisect
import time

cave_map = []

class Path():
    def __init__(self, cost: int, path_list: list, current_point: tuple):
        self.cost = cost
        self.path_list = path_list
        self.current_point = current_point

    def find_candidates(self):
        global cave_map
        moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        points = [(self.current_point[0] + x, self.current_point[1] + y) for x, y in moves]
        points = list(filter(lambda point: point[0] >= 0 and point[0] < len(cave_map) and point[1] >= 0 and point[1] < len(cave_map[0]) and point not in self.path_list, points))
        candidates = [self.candidate_point_to_path(point) for point in points]
        return candidates
        

    def candidate_point_to_path(self, candidate: tuple):
        return Path(self.cost + cave_map[candidate[0]][candidate[1]], self.path_list + [candidate], candidate)


    def step(self, past_candidates: list):
        global cave_map
        target = (len(cave_map) - 1, len(cave_map[0]) -1)
        if self.current_point == target:
            return [self]
        candidates = self.find_candidates()
        all_candidates = past_candidates.copy()
        for candidate in candidates:
            bisect.insort(all_candidates, candidate)
        return all_candidates

    def __str__(self) -> str:
        global cave_map
        x_len = len(cave_map)
        y_len = len(cave_map[0])
        res = ""
        for y in range(y_len):
            line = ""
            for x in range(x_len):
                point = str(cave_map[x][y])
                point_str = f"[{point}]" if (x, y) in self.path_list else f" {point} "
                line += point_str
            res += "\n" + line
        return res[1:]

    def get_distance(self):
        global cave_map
        max_x = len(cave_map) - 1
        max_y = len(cave_map[0]) - 1
        return (max_x - self.current_point[0]) + (max_y - self.current_point[1])

    def get_weighted_cost(self):
        return self.cost + 3 * self.get_distance()

    def __eq__(self, other) -> bool:
        return self.get_weighted_cost() == other.get_weighted_cost()

    def __lt__(self, other):
        return self.get_weighted_cost() < other.get_weighted_cost()

    def __le__(self, other):
        return self.get_weighted_cost() <= other.get_weighted_cost()

    def __gt__(self, other):
        return self.get_weighted_cost() > other.get_weighted_cost()

    def __ge__(self, other):
        return self.get_weighted_cost() >= other.get_weighted_cost()


def parse_input(filename: str):
    global cave_map
    with open(filename, mode="r") as input:
        lines = [[int(char) for char in line.strip()] for line in input.readlines()]
        y_len = len(lines)
        x_len = len(lines[0])
        for x in range(x_len):
            if len(cave_map) <= x:
                cave_map.append([])
            for y in range(y_len):
                cave_map[x].append(lines[y][x])

def print_map():
    global cave_map
    x_len = len(cave_map)
    y_len = len(cave_map[0])
    for y in range(y_len):
        line = ""
        for x in range(x_len):
            line += str(cave_map[x][y])
        print(line)



parse_input("input-15-test")
current = Path(0, [(0,0)], (0,0))
target = (len(cave_map) - 1, len(cave_map[0]) -1)
print(target)
candidates = []

start = time.perf_counter_ns()
while(True):
    candidates = current.step(candidates)
    if len(candidates) == 1:
        final_path = candidates[0]
        print(final_path)
        print()
        print(f"Path cost: {final_path.cost}")
        end = time.perf_counter_ns()
        duration = int((end - start) / 1_000_000)
        print(f"Duration: {duration}ms")
        break
    current = candidates.pop(1)
    # print()
    # print(current)



