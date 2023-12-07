from functools import reduce

class Race:
    def __init__(self, time: int, distance: int) -> None:
        self.time = time
        self.distance = distance

    def __repr__(self) -> str:
        return f'Time: {self.time}; Distance: {self.distance}'

def calc_distance(charge_time: int, total_time: int) -> int:
    remaining_time = total_time - charge_time
    return charge_time * remaining_time

def beat_race(race: Race) -> int:
    min_win = 0
    for charge_time in range(1, race.time):
        distance = calc_distance(charge_time, race.time)
        if distance > race.distance:
            min_win = charge_time
            break

    max_win = 0
    for charge_time in range(race.time - 1, 0, -1):
        distance = calc_distance(charge_time, race.time)
        if distance > race.distance:
            max_win = charge_time
            break

    return max_win - min_win + 1

def parse_input(filename: str):
    with open(filename, 'r') as file:
        time_line = file.readline()
        time_line = time_line[time_line.find(':') + 1:].strip()
        time = int(time_line.replace(' ', ''))

        distance_line = file.readline()
        distance_line = distance_line[distance_line.find(':') + 1:].strip()
        distance = int(distance_line.replace(' ', ''))

        return Race(time, distance)

race = parse_input('input-06')
print(race)
win_counts = beat_race(race)
print(win_counts)