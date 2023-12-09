from itertools import pairwise

class Row:
    def __init__(self, numbers: list[int]) -> None:
        self.numbers = numbers

    def __repr__(self) -> str:
        return str(self.numbers)

    def is_terminal(self):
        unique_numbers = set(self.numbers)
        if len(unique_numbers) == 1 and 0 in unique_numbers:
            return True
        return False
    
    def calc_deltas(self):
        deltas = []
        for left, right in pairwise(self.numbers):
            deltas.append(right - left)
        return Row(deltas)
    
    def extrapolate_next_value(self) -> int:
        if self.is_terminal():
            return 0
        deltas = self.calc_deltas()
        return self.numbers[-1] + deltas.extrapolate_next_value()
    
    def extrapolate_left(self) -> int:
        if self.is_terminal():
            return 0
        deltas = self.calc_deltas()
        return self.numbers[0] - deltas.extrapolate_left()

def parse_input(filename: str) -> list[Row]:
    rows = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            numbers = [int(val) for val in line.split()]
            rows.append(Row(numbers))
    return rows

rows = parse_input('input-09')
result = sum([row.extrapolate_left() for row in rows])
print(result)