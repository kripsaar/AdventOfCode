import math
import itertools
import numpy as np

alternate_bases = []
# inverse = {np.array([[1,0,0],[0,1,0],[0,0,1]]): np.linalg.inv(np.array([[1,0,0],[0,1,0],[0,0,1]]))}
scanner_base = {}
scanner_pos = {}

def init_bases():
    alternate_bases.append(np.array([[1,0,0],[0,1,0],[0,0,1]]))
    alternate_bases.append(np.array([[1,0,0],[0,0,1],[0,1,0]]))
    alternate_bases.append(np.array([[0,1,0],[1,0,0],[0,0,1]]))
    alternate_bases.append(np.array([[0,1,0],[0,0,1],[1,0,0]]))
    alternate_bases.append(np.array([[0,0,1],[1,0,0],[0,1,0]]))
    alternate_bases.append(np.array([[0,0,1],[0,1,0],[1,0,0]]))
    
    alternate_bases.append(np.array([[-1,0,0],[0,1,0],[0,0,1]]))
    alternate_bases.append(np.array([[-1,0,0],[0,0,1],[0,1,0]]))
    alternate_bases.append(np.array([[0,1,0],[-1,0,0],[0,0,1]]))
    alternate_bases.append(np.array([[0,1,0],[0,0,1],[-1,0,0]]))
    alternate_bases.append(np.array([[0,0,1],[-1,0,0],[0,1,0]]))
    alternate_bases.append(np.array([[0,0,1],[0,1,0],[-1,0,0]]))

    alternate_bases.append(np.array([[1,0,0],[0,-1,0],[0,0,1]]))
    alternate_bases.append(np.array([[1,0,0],[0,0,1],[0,-1,0]]))
    alternate_bases.append(np.array([[0,-1,0],[1,0,0],[0,0,1]]))
    alternate_bases.append(np.array([[0,-1,0],[0,0,1],[1,0,0]]))
    alternate_bases.append(np.array([[0,0,1],[1,0,0],[0,-1,0]]))
    alternate_bases.append(np.array([[0,0,1],[0,-1,0],[1,0,0]]))
    
    alternate_bases.append(np.array([[1,0,0],[0,1,0],[0,0,-1]]))
    alternate_bases.append(np.array([[1,0,0],[0,0,-1],[0,1,0]]))
    alternate_bases.append(np.array([[0,1,0],[1,0,0],[0,0,-1]]))
    alternate_bases.append(np.array([[0,1,0],[0,0,-1],[1,0,0]]))
    alternate_bases.append(np.array([[0,0,-1],[1,0,0],[0,1,0]]))
    alternate_bases.append(np.array([[0,0,-1],[0,1,0],[1,0,0]]))
    
    alternate_bases.append(np.array([[-1,0,0],[0,-1,0],[0,0,1]]))
    alternate_bases.append(np.array([[-1,0,0],[0,0,1],[0,-1,0]]))
    alternate_bases.append(np.array([[0,-1,0],[-1,0,0],[0,0,1]]))
    alternate_bases.append(np.array([[0,-1,0],[0,0,1],[-1,0,0]]))
    alternate_bases.append(np.array([[0,0,1],[-1,0,0],[0,-1,0]]))
    alternate_bases.append(np.array([[0,0,1],[0,-1,0],[-1,0,0]]))
    
    alternate_bases.append(np.array([[-1,0,0],[0,1,0],[0,0,-1]]))
    alternate_bases.append(np.array([[-1,0,0],[0,0,-1],[0,1,0]]))
    alternate_bases.append(np.array([[0,1,0],[-1,0,0],[0,0,-1]]))
    alternate_bases.append(np.array([[0,1,0],[0,0,-1],[-1,0,0]]))
    alternate_bases.append(np.array([[0,0,-1],[-1,0,0],[0,1,0]]))
    alternate_bases.append(np.array([[0,0,-1],[0,1,0],[-1,0,0]]))
    
    alternate_bases.append(np.array([[1,0,0],[0,-1,0],[0,0,-1]]))
    alternate_bases.append(np.array([[1,0,0],[0,0,-1],[0,-1,0]]))
    alternate_bases.append(np.array([[0,-1,0],[1,0,0],[0,0,-1]]))
    alternate_bases.append(np.array([[0,-1,0],[0,0,-1],[1,0,0]]))
    alternate_bases.append(np.array([[0,0,-1],[1,0,0],[0,-1,0]]))
    alternate_bases.append(np.array([[0,0,-1],[0,-1,0],[1,0,0]]))
    
    alternate_bases.append(np.array([[-1,0,0],[0,-1,0],[0,0,-1]]))
    alternate_bases.append(np.array([[-1,0,0],[0,0,-1],[0,-1,0]]))
    alternate_bases.append(np.array([[0,-1,0],[-1,0,0],[0,0,-1]]))
    alternate_bases.append(np.array([[0,-1,0],[0,0,-1],[-1,0,0]]))
    alternate_bases.append(np.array([[0,0,-1],[-1,0,0],[0,-1,0]]))
    alternate_bases.append(np.array([[0,0,-1],[0,-1,0],[-1,0,0]]))

    # for base in alternate_bases:
    #     inverse[base] = np.linalg.inv(base)

class Beacon:
    def __init__(self, base_scanner, pos):
        self.base_scanner = base_scanner
        self.pos = {}
        self.pos[base_scanner] = pos
        self.distance_map = {}

    def __repr__(self) -> str:
        return str(self.pos)

    def find_common_scanner(self, other):
        self_scanners = set(self.pos.keys())
        other_scanners = set(other.pos.keys())
        return self_scanners.intersection(other_scanners).pop()

    def find_distance(self, other):
        scanner = self.find_common_scanner(other)
        distance = self.calc_distance(self.pos[scanner], other.pos[scanner])
        self.distance_map[other] = distance
        other.distance_map[self] = distance
        return distance

    def calc_distance(self, self_pos, pos):
        x, y, z = self_pos
        ox, oy, oz = pos
        distance = math.sqrt((ox - x) ** 2 + (oy - y) ** 2 + (oz - z) ** 2)
        return distance

    def absorb_beacon(self, other):
        for scanner, pos in other.pos.items():
            self.pos[scanner] = pos
        known_distances = set(self.distance_map.values())
        for beacon, distance in other.distance_map.items():
            if distance in known_distances:
                continue
            self.distance_map[beacon] = distance
            beacon.distance_map.pop(other, None)
            beacon.distance_map[self] = distance



    def is_same_beacon(self, other):
        distances = set(self.distance_map.values())
        other_distances = set(other.distance_map.values())
        intersection = distances.intersection(other_distances)
        if len(intersection) >= 4:
            self.absorb_beacon(other)
            return True
        else:
            return False

def parse_input(filename: str):
    with open(filename, mode="r") as input:
        scanners = [part.strip() for part in input.read().split("\n\n")]
        scanner_beacons = {}
        for index, scanner in enumerate(scanners):
            scanner_beacons[index] = []
            scanner = scanner.strip().splitlines()
            for beacon_string in scanner[1:]:
                pos = [int(item) for item in beacon_string.strip().split(",")]
                beacon = Beacon(index, (pos[0], pos[1], pos[2]))
                scanner_beacons[index].append(beacon)
            for pair in itertools.combinations(scanner_beacons[index], 2):
                pair[0].find_distance(pair[1])
        return scanner_beacons

def match_scanners(left_scanner_beacons: list, right_scanner_beacons: list):
    combined_beacons = []
    for beacon in left_scanner_beacons:
        for other_beacon in right_scanner_beacons.copy():
            if beacon.is_same_beacon(other_beacon):
                right_scanner_beacons.remove(other_beacon)
        combined_beacons.append(beacon)
    # leftovers
    for other_beacon in right_scanner_beacons:
        combined_beacons.append(other_beacon)
    return combined_beacons

def find_beacons_for_scanners(beacon_list: list, left_scanner: int, right_scanner: int):
    res = []
    for beacon in beacon_list:
        if left_scanner in beacon.pos and right_scanner in beacon.pos:
            res.append(beacon)
    return res

def find_scanner_pos(all_beacons: list, origin_scanner: int, target_scanner: int):
    beacons = find_beacons_for_scanners(all_beacons, origin_scanner, target_scanner)
    if len(beacons) < 2:
        # not enough overlapping beacons for a direct conversion, need to go over another step
        base_keys = list(filter(lambda x: x[1] == origin_scanner, scanner_base.keys()))
        if len(base_keys) == 0:
            return None
        for base_key in base_keys:
            base = scanner_base[base_key]
            step = find_scanner_pos(all_beacons, base_key[0], target_scanner)
            if step is None:
                continue
            target = scanner_pos[(base_key[0], origin_scanner)] + base.dot(step)
            return target
        return None
    for base in alternate_bases:
        candidate = np.array(beacons[0].pos[origin_scanner]).transpose() - base.dot(np.array(beacons[0].pos[target_scanner]).transpose())
        failed = False
        for beacon in beacons:
            original_pos = np.array(beacon.pos[origin_scanner]).transpose()
            target_pos = np.array(beacon.pos[target_scanner]).transpose()
            attempt = candidate + base.dot(target_pos)
            if not np.array_equal(attempt, original_pos):
                failed = True
                break
        if failed:
            continue
        else:
            scanner_base[(target_scanner, origin_scanner)] = base
            scanner_pos[(target_scanner, origin_scanner)] = candidate
            return candidate

def get_manhattan_distance(pos1: np.ndarray, pos2: np.ndarray) -> int:
    distance = np.abs(pos1 - pos2).sum()
    print(f"Manhattan distance between {pos1} and {pos2} = {distance}")
    return distance

init_bases()

scanner_beacons = parse_input("input-19")

beacon_sets = list(scanner_beacons.values())
new_beacon_sets = []
for pair in itertools.combinations(beacon_sets, 2):
    new_beacon_sets.append(match_scanners(pair[0], pair[1]))

main_set = new_beacon_sets[0]
beacon_sets = new_beacon_sets[1:]
for other_set in beacon_sets:
    new_main_set = match_scanners(main_set, other_set)
    main_set = new_main_set

old_len = float("inf")
while old_len > len(main_set):
    old_len = len(main_set)
    main_set = match_scanners(main_set, main_set)

scanners = list(scanner_beacons.keys())
scanners.remove(0)
positions = [np.array([0,0,0]).transpose()]
while len(scanners) > 0:
    scanner = scanners.pop(0)
    pos = find_scanner_pos(main_set, 0, scanner)
    if pos is None:
        scanners.append(scanner)
        continue
    positions.append(pos)
    
print(f"Positions count: {len(positions)}")

distances = []
for pair in itertools.combinations(positions, 2):
    distance = get_manhattan_distance(pair[0], pair[1])
    distances.append(distance)

print(f"Max distance: {max(distances)}")