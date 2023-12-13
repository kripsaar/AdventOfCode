import re

class Record:
    def __init__(self, record_str: str, dmg_list: list[int], regex_pattern: str) -> None:
        self.record_str = record_str
        self.dmg_list = dmg_list
        self.regex_pattern = regex_pattern

    def __repr__(self) -> str:
        result = self.record_str + ' '
        for dmg in self.dmg_list:
            result += f'{dmg},'
        return result[:-1]

    def is_valid(self) -> bool:
        match = re.match(self.regex_pattern, self.record_str)
        if match:
            return True
        else:
            return False

    def find_all_configurations(self) -> list:
        if '?' not in self.record_str:
            return [self]
        result = []
        for replacement in ('#', '.'):
            new_record_str = self.record_str.replace('?', replacement, 1)
            new_record = Record(new_record_str, self.dmg_list, self.regex_pattern)
            if not new_record.is_valid():
                continue
            result.extend(new_record.find_all_configurations())
        return result
        
def generate_regex_pattern(dmg_list: list[int]):
    dot_pattern = '(?:\.|\?)'
    hash_pattern = '(?:#|\?)'
    pattern = f'^'
    for dmg in dmg_list:
        pattern += f'{dot_pattern}+{hash_pattern}{{{dmg}}}'
    pattern = pattern.replace('+', '*', 1)
    pattern += f'{dot_pattern}*$'
    return pattern

def parse_input(filename: str):
    records: list[Record] = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            record_str, dmg_list_str = line.split()
            dmg_list = [int(dmg) for dmg in dmg_list_str.split(',')]
            regex_pattern = generate_regex_pattern(dmg_list)
            records.append(Record(record_str, dmg_list, regex_pattern))
    return records

records = parse_input('input-12')
sum = 0
for record in records:
    all_configs = record.find_all_configurations()
    sum += len(all_configs)
print(sum)