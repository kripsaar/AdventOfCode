class Card:
    def __init__(self,name: str, id: int, winning_numbers: list, numbers: list) -> None:
        self.name = name
        self.id = id
        self.winning_numbers = winning_numbers
        self.numbers = numbers
        self.count = 1

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
    
    def add_copies(self, copy_count: int):
        self.count += copy_count

    def generate_copies(self):
        matching_numbers = list(set(self.winning_numbers).intersection(self.numbers))
        result = []
        for i in range(1, len(matching_numbers) + 1):
            result.append(self.id + i)
        return result


def parse_numbers(numbers_str: str):
    return [int(num_str) for num_str in numbers_str.split()]

def parse_line(line: str) -> Card:
    colon_pos = line.find(':')
    name = line[:colon_pos]
    card_id = int(name.split()[1])
    winning_numbers_str, numbers_str = line[colon_pos+2:].split(' | ')
    return Card(name, card_id, parse_numbers(winning_numbers_str), parse_numbers(numbers_str))


def parse_input(filename: str) -> dict[int, Card]:
    cards = {}
    with open(filename, 'r') as file:
        for line in file.readlines():
            card = parse_line(line)
            cards[card.id] = card
    return cards

cards = parse_input('input-04')
for card in cards.values():
    copies = card.generate_copies()
    for copy_id in copies:
        cards[copy_id].count += card.count

total_card_count = sum([card.count for card in cards.values()])
print(total_card_count)