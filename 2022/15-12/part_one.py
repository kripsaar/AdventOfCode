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

def mark_covered(sensor: Sensor, target_y, marked: set):
    x, y = sensor.pos
    y_dist = abs(y - target_y)
    if y_dist > sensor.distance_to_beacon:
        return
    diff = sensor.distance_to_beacon - y_dist
    for x_offset in range(-diff, diff + 1):
        marked.add(x + x_offset)
         
def mark_beacon(sensor: Sensor, target_y, beacons: set):
    x, y = sensor.closest_beacon
    if y == target_y:
        beacons.add(x)

target_y = 2000000
filename = 'input-15'
sensors = parse_input(filename)

marked = set()
beacons = set()

for sensor in sensors:
    mark_covered(sensor, target_y, marked)
    mark_beacon(sensor, target_y, beacons)

marked.difference_update(beacons)

print(len(marked))

