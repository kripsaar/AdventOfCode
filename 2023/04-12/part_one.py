class Card:
    def __init__(self, name: str, winning_numbers: list, numbers: list) -> None:
        self.name = name
        self.winning_numbers = winning_numbers
        self.numbers = numbers

    def __repr__(self):
        result = f'{self.name}:'
        for num in self.winning_numbers:
            result += f' {num}'.rjust(3)
        result += ' |'
        for num in self.numbers:
            result += f' {num}'.rjust(3)
        return result
    
    def score(self) -> int:
        matching_numbers = list(set(self.winning_numbers).intersection(self.numbers))
        if not matching_numbers:
            return 0
        return 2 ** (len(matching_numbers) - 1)

def parse_numbers(numbers_str: str):
    return [int(num_str) for num_str in numbers_str.split()]

def parse_line(line: str) -> Card:
    colon_pos = line.find(':')
    name = line[:colon_pos]
    winning_numbers_str, numbers_str = line[colon_pos+2:].split(' | ')
    return Card(name, parse_numbers(winning_numbers_str), parse_numbers(numbers_str))


def parse_input(filename: str):
    cards = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            card = parse_line(line)
            cards.append(card)
    return cards

cards = parse_input('input-04')
score = sum([card.score() for card in cards])
print(score)