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
    count = 0
    for charge_time in range(1, race.time):
        if calc_distance(charge_time, race.time) > race.distance:
            count += 1
    return count


def parse_input(filename: str):
    with open(filename, 'r') as file:
        time_line = file.readline()
        time_line = time_line[time_line.find(':') + 1:].strip()
        times = [int(time_str) for time_str in time_line.split()]

        distance_line = file.readline()
        distance_line = distance_line[distance_line.find(':') + 1:].strip()
        distances = [int(distance_str) for distance_str in distance_line.split()]

        races = [Race(time, distance) for (time, distance) in zip(times, distances)]
        return races

races = parse_input('input-06')
win_counts = [beat_race(race) for race in races]
result = reduce(lambda a, b: a * b, win_counts)
print(result)