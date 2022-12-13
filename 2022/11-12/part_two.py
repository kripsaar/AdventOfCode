from typing import List

class Monkey:
    def __init__(self, items: list[int], operation, test, target_true: int, target_false: int, monkeys) -> None:
        self.items = items
        self.operation = operation
        self.test = test
        self.target_true = target_true
        self.target_false = target_false
        self.inspect_count = 0
        self.monkeys = monkeys
        self.modulo = None

    def throw(self, item: int, target: int):
        if self.modulo:
            item = item % self.modulo
        target_monkey = self.monkeys[target]
        target_monkey.items.append(item)

    def take_turn(self):
        for item in self.items:
            item = self.operation(item)
            self.inspect_count += 1
            if self.test(item):
                self.throw(item, self.target_true)
            else:
                self.throw(item, self.target_false)
        self.items = []

def parse_title(line: str):
    line = line.lstrip('Monkey ').rstrip(':')
    return int(line)

def parse_items(line: str):
    return [int(item) for item in line[18:].split(', ')]

def parse_operation(line: str):
    operator, second = line[23:].split(' ')
    if operator == '*':
        if second == 'old':
            return lambda x: x * x
        else:
            return lambda x: x * int(second)
    else:
        if second == 'old':
            return lambda x: x + x
        else:
            return lambda x: x + int(second)

def parse_test(line: str):
    divisor = int(line[21:])
    return lambda x: x % divisor == 0

def parse_target_true(line: str):
    return int(line[29])

def parse_target_false(line: str):
    return int(line[30])

def parse_input(filename: str):
    monkeys = dict()
    modulo = 1
    with open(filename, mode='r') as file:
        for part in file.read().split('\n\n'):
            lines = part.splitlines()
            monkey_no = parse_title(lines[0])
            items = parse_items(lines[1])
            operation = parse_operation(lines[2])
            test = parse_test(lines[3])
            target_true = parse_target_true(lines[4])
            target_false = parse_target_false(lines[5])
            divisor = int(lines[3][21:])
            modulo *= divisor
            monkeys[monkey_no] = Monkey(items, operation, test, target_true, target_false, monkeys)
    for monkey in monkeys.values():
        monkey.modulo = modulo
    return monkeys

def sort_monkeys(monkeys: dict):
    values = monkeys.values()
    return sorted(values, reverse=True, key=lambda x: x.inspect_count)


filename = "input-11"
monkeys = parse_input(filename)

round_count = 10000
for round in range(0, round_count):
    for monkey in monkeys.values():
        monkey.take_turn()

sorted_monkeys = sort_monkeys(monkeys)
monkey_business = sorted_monkeys[0].inspect_count * sorted_monkeys[1].inspect_count
print(monkey_business)