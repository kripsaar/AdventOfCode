import time
from collections import deque

class Sensor:
    def __init__(self, pos, closest_beacon) -> None:
        self.pos = pos
        self.closest_beacon = closest_beacon
        self.distance_to_beacon = calc_distance(pos, closest_beacon)

    def __repr__(self) -> str:
        return f"{self.pos} - {self.closest_beacon}"
    
def calc_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def parse_input(filename: str):
    beacons = []
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            sensor_x = int(line[line.find('x=') + 2:line.find(', ')])
            sensor_y = int(line[line.find('y=') + 2:line.find(': ')])
            beacon_x = int(line[line.rfind('x=') + 2:line.rfind(', ')])
            beacon_y = int(line[line.rfind('y=') + 2:])
            beacons.append(Sensor((sensor_x, sensor_y), (beacon_x, beacon_y)))
    return beacons

def remove_candidates(sensor: Sensor, candidate_y, candidates: set):
    x, y = sensor.pos
    y_dist = abs(y - candidate_y)
    if y_dist > sensor.distance_to_beacon:
        return
    diff = sensor.distance_to_beacon - y_dist
    # for x_offset in range(-diff, diff + 1):
    candidates.difference_update(range(x - diff, x + diff + 1))

def get_exclusion_range(sensor: Sensor, candidate_y, ranges: list):
    x, y = sensor.pos
    y_dist = abs(y - candidate_y)
    if y_dist > sensor.distance_to_beacon:
        return
    diff = sensor.distance_to_beacon - y_dist
    ranges.append(range(x - diff, x + diff + 1))

def ranges_overlap(left: range, right: range) -> bool:
    return left.start < right.stop and left.stop > right.start

def merge_ranges(ranges: list):
    if not ranges:
        return ranges
    ranges = sorted(ranges, key=lambda r: r.start)
    working_list = deque(ranges)
    result_list = []
    while working_list:
        left = working_list.popleft()
        while working_list and ranges_overlap(left, working_list[0]):
            right = working_list.popleft()
            left = range(min(left.start, right.start), max(left.stop, right.stop))
        result_list.append(left)
    return result_list
        

         
max_coord = 4000000
# max_coord = 20
modulo = 10000
filename = 'input-15'
sensors = parse_input(filename)

result = None
candidates = set()
candidates_template = set(range(0, max_coord))

start = time.time()
for y in range(0, max_coord):
    ranges = []
    for sensor in sensors:
        get_exclusion_range(sensor, y, ranges)
    ranges = merge_ranges(ranges)
    if y % modulo == 0:
        end = time.time()
        print(f"Progress: {y}/{max_coord} ({int((y / max_coord) * 100)}%)")
        print(f"Avg time per loop: {int(((end - start) * 1000) / modulo)}ms")
        start = end
    if len(ranges) > 1:
        candidates = candidates_template.copy()
        for sensor in sensors:
            remove_candidates(sensor, y, candidates)
        result = (candidates.pop(), y)
        break

x, y = result
tuning_frequency = x * 4000000 + y
print(tuning_frequency)