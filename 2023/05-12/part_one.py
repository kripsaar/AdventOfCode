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
    
class Map:
    def __init__(self, ranges: list[MapRange]) -> None:
        self.ranges = ranges

    def get(self, key) -> int:
        for range in self.ranges:
            if not range.is_in_range(key):
                continue
            return range.get(key)
        return key

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
        seeds = [int(seed) for seed in (seeds_line[seeds_line.find(':') + 2:]).split()]

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

parse_input('input-05')
locations = [travel_to_destination(seed) for seed in seeds]
print(f'Lowest location numbner: {min(locations)}')