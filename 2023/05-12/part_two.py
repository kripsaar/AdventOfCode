import time

class MapRange:
    def __init__(self, source_start: int, dest_start: int, range_length: int) -> None:
        self.source_start = source_start
        self.dest_start = dest_start
        self.range_length = range_length

    def is_in_range(self, key: int) -> bool:
        if key >= self.source_start and key < self.source_start + self.range_length:
            return True
        return False
    
    def get(self, key: int) -> int:
        if not self.is_in_range(key):
            return key
        diff = key - self.source_start
        return self.dest_start + diff
    
    def get_overlap(self, range_to_check: range) -> range:
        return range(max(self.source_start, range_to_check.start), min(self.source_start + self.range_length, range_to_check.stop))
    
    def map_range(self, range_to_map: range) -> range:
        overlap = self.get_overlap(range_to_map)
        offset = overlap.start - self.source_start
        return range(self.dest_start + offset, self.dest_start + offset + len(overlap))
    
class Map:
    def __init__(self, ranges: list[MapRange]) -> None:
        self.ranges = ranges

    def get(self, key) -> int:
        for range in self.ranges:
            if not range.is_in_range(key):
                continue
            return range.get(key)
        return key
    
    def map_ranges(self, ranges_to_map: list[range]) -> list[range]:
        resulting_ranges = []
        working_list = [range_to_map for range_to_map in ranges_to_map]
        while working_list:
            current_range = working_list.pop(0)
            mapped_range: range = None
            for map_range in self.ranges:
                overlap = map_range.get_overlap(current_range)
                if len(overlap) <= 0:
                    continue
                mapped_range = map_range.map_range(overlap)
                resulting_ranges.append(mapped_range)
                remainder = range_diff(current_range, overlap)
                working_list.extend(remainder)
                break
            if not mapped_range:
                resulting_ranges.append(current_range)
        return resulting_ranges


def range_diff(lrange: range, rrange: range):
    result = []
    if lrange.start < rrange.start:
        result.append(range(lrange.start, min(rrange.start, lrange.stop)))
    if rrange.stop < lrange.stop:
        result.append(range(rrange.stop, lrange.stop))
    return result

seeds = []
seed_to_soil: Map = None
soil_to_fertilizer: Map = None
fertilizer_to_water: Map = None
water_to_light: Map = None
light_to_temperature: Map = None
temperature_to_humidity: Map = None
humidity_to_location: Map = None

def parse_map_line(line: str) -> MapRange:
    dest_start, source_start, range_length = [int(val) for val in line.split()]
    return MapRange(source_start, dest_start, range_length)

def parse_input(filename: str):
    global seeds
    global seed_to_soil
    global soil_to_fertilizer
    global fertilizer_to_water
    global water_to_light
    global light_to_temperature
    global temperature_to_humidity
    global humidity_to_location

    with open(filename, 'r') as file:
        seeds_line = file.readline().strip()
        seeds_line = seeds_line[seeds_line.find(':') + 2:]
        seeds_split = seeds_line.split()
        seeds = [range(int(seed_start), int(seed_start) + int(range_length)) for (seed_start, range_length) in zip(seeds_split[::2], seeds_split[1::2])]

        file.readline()
        file.readline()
        seed_to_soil_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            seed_to_soil_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        seed_to_soil = Map(seed_to_soil_ranges)

        file.readline()
        soil_to_fertilizer_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            soil_to_fertilizer_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        soil_to_fertilizer = Map(soil_to_fertilizer_ranges)

        file.readline()
        fertilizer_to_water_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            fertilizer_to_water_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        fertilizer_to_water = Map(fertilizer_to_water_ranges)

        file.readline()
        water_to_light_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            water_to_light_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        water_to_light = Map(water_to_light_ranges)

        file.readline()
        light_to_temperature_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            light_to_temperature_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        light_to_temperature = Map(light_to_temperature_ranges)

        file.readline()
        temperature_to_humidity_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            temperature_to_humidity_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        temperature_to_humidity = Map(temperature_to_humidity_ranges)

        file.readline()
        humidity_to_location_ranges = []
        line = file.readline().strip()
        while len(line.strip()) > 0: 
            humidity_to_location_ranges.append(parse_map_line(line))
            line = file.readline().strip()
        humidity_to_location = Map(humidity_to_location_ranges)
        
def travel_to_destination(seed_number: int) -> int:
    soil = seed_to_soil.get(seed_number)
    fertilizer = soil_to_fertilizer.get(soil)
    water = fertilizer_to_water.get(fertilizer)
    light = water_to_light.get(water)
    temperature = light_to_temperature.get(light)
    humidity = temperature_to_humidity.get(temperature)
    location = humidity_to_location.get(humidity)
    return location

def travel_to_destination_ranges(seed_ranges: list[range]) -> list[range]:
    soil_ranges = seed_to_soil.map_ranges(seed_ranges)
    fertilizer_ranges = soil_to_fertilizer.map_ranges(soil_ranges)
    water_ranges = fertilizer_to_water.map_ranges(fertilizer_ranges)
    light_ranges = water_to_light.map_ranges(water_ranges)
    temperature_ranges = light_to_temperature.map_ranges(light_ranges)
    humidity_ranges = temperature_to_humidity.map_ranges(temperature_ranges)
    location_ranges = humidity_to_location.map_ranges(humidity_ranges)
    return location_ranges

start = time.time()

parse_input('input-05')

location_ranges = travel_to_destination_ranges(seeds)
final_destination = min([location_range.start for location_range in location_ranges])
print(f'Lowest location numbner: {final_destination}')

end = time.time()
print(f"Runtime: {int(((end - start) * 1000))}ms")