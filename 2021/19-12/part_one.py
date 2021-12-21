import math
import itertools
import numpy as np

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

print()
for item in main_set:
    print(item)
print()
print(f"len : {len(main_set)}")

# print(f"Found {len(result_beacons)} overlapping beacons: ")
# print(result_beacons)


# print()
# print(result_beacons[0])
# print(result_beacons[1])
# print(result_beacons[2])
# print()

# desu = find_lin_independent_vectors([item[0].pos for item in result_beacons])
# desu = [result_beacons[0][0].pos, result_beacons[1][0].pos, result_beacons[2][0].pos]
# print(f"Desu: {desu}")
# uguu = find_lin_independent_vectors([item[1].pos for item in result_beacons])
# uguu = [result_beacons[0][1].pos, result_beacons[1][1].pos, result_beacons[2][1].pos]
# print(f"Uguu: {uguu}")

# X = np.array([desu[0], desu[1], desu[2]]).transpose()
# print(f"X = {X}")
# Xo = np.array([uguu[0], uguu[1], uguu[2]]).transpose()
# print(f"X' = {Xo}")
# X_inverse = np.linalg.inv(X)
# print(f"X^-1 = {X_inverse}")

# A = Xo.dot(X_inverse)
# print(f"A = {A}")
# A_inverse = np.linalg.inv(A)
# print(f"A^-1 = {A_inverse}")

# test = A_inverse.dot(np.array([-460, 603, -452]).transpose())
# print(f"Test point = {test}")

# scanner_one = A_inverse.dot(np.array([0,0,0]).transpose())

# print(scanner_one)

# for pair in result_beacons:
#     print(pair)
