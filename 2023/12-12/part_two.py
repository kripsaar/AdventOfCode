import time
from functools import cache

class Record:
    def __init__(self, record_str: str, dmg_list: list[int]) -> None:
        self.record_str = record_str
        self.dmg_list = dmg_list

    def __repr__(self) -> str:
        result = self.record_str + ' '
        for dmg in self.dmg_list:
            result += f'{dmg},'
        return result[:-1]
    
    def __eq__(self, other: object) -> bool:
        if self.record_str == other.record_str:
            return True

    def __hash__(self) -> int:
        return hash(str(self))

    def find_all_configurations(self) -> list:
        return place_current_target(self.record_str, tuple(self.dmg_list))

@cache
def place_current_target(current_substr: str, targets: tuple[int]):
    current_target = targets[0]
    rest = targets[1:]
    ignore_tail = sum(rest) + len(rest)

    count = 0

    for before in range(len(current_substr) - ignore_tail - current_target + 1):
        # potential match
        if all(char in '?#' for char in current_substr[before : before + current_target]):
            if not rest:
                if all(char in '?.' for char in current_substr[before + current_target:]):
                    # If no more targets, and the rest is all clear
                    count += 1
            if len(rest) > 0 and current_substr[before + current_target] in '?.':
                # Next character after match is legal
                count += place_current_target(current_substr[before + current_target + 1:], rest)

        # no match, but still #
        if current_substr[before] == '#':
            break

    return count

def unfold_record_str(record_str: str, unfold_multiplier: int) -> str:
    return ((record_str + '?') * unfold_multiplier)[:-1]

def parse_input(filename: str, unfold_multiplier: int):
    records: list[Record] = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            record_str, dmg_list_str = line.split()
            record_str = unfold_record_str(record_str, unfold_multiplier)
            dmg_list = [int(dmg) for dmg in dmg_list_str.split(',')] * unfold_multiplier
            records.append(Record(record_str, dmg_list))
    return records

start = time.time()

records = parse_input('input-12', 5)

config_sum = 0
timed_records = []
for idx, record in enumerate(records):
    original_line = idx + 1
    record_start = time.time()
    config_count = record.find_all_configurations()
    config_sum += config_count
    record_end = time.time()
    record_runtime = int(((record_end - record_start) * 1000))
    print(f"{original_line}: {record} - {config_count} arrangements [{record_runtime}ms]")
    timed_records.append((record_runtime, record, config_count, original_line))

timed_records.sort(key=lambda tuple: tuple[0])
for record_runtime, record, config_count, original_line in timed_records:
    print(f"{original_line}: {record} - {config_count} arrangements [{record_runtime}ms]")
    
print(config_sum)

end = time.time()
print(f"Runtime: {int(((end - start) * 1000))}ms")