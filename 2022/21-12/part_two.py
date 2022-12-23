from __future__ import annotations
import re

def parse_input(filename: str):
    monkeys = dict()
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            line = line.strip().split(': ')
            value = line[1]
            if value.isnumeric():
                value = int(value)
            monkeys[line[0]] = value
    return monkeys

class Term:
    def __init__(self, name: str, value: int = None, left: Term = None, right: Term = None, operator: str = None) -> None:
        self.name = name
        self.value = value
        self.left = left
        self.right = right
        self.operator = operator

    def __repr__(self) -> str:
        if self.name == 'humn':
            return 'humn'
        if self.value is not None:
            return str(self.value)
        else:
            return f"({self.left} {self.operator} {self.right})"

    def contains_humn(self):
        if self.name == 'humn':
            return True
        if self.value is not None:
            return False
        if self.left.contains_humn() or self.right.contains_humn():
            return True

    def evaluate(self) -> int:
        if self.name == 'humn':
            return 2022
        if self.value is not None:
            return self.value
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        if self.operator == '+':
            self.value = left_val + right_val
            return self.value
        if self.operator == '-':
            self.value = left_val - right_val
            return self.value
        if self.operator == '*':
            self.value = left_val * right_val
            return self.value
        if self.operator == '/':
            self.value = int(left_val / right_val)
            return self.value
        if self.operator == '=':
            if left_val < right_val:
                return -1
            if left_val > right_val:
                return 1
            else:
                return 0

    def solve_step(self):
        if self.left.contains_humn():
            if self.left.name == 'humn':
                # done
                return False
            # move from left side to right
            self.move_left_to_right()
        else:
            if self.right.name == 'humn':
                # done
                return False
            # move from right side to left
            self.move_right_to_left()
        return True

    def solve(self):
        while self.solve_step():
            pass
        print(self)

    def move_left_to_right(self):
        term_to_move: Term
        operator = opposite_operator(self.left.operator)
        if self.left.right.contains_humn() and not (self.left.operator == '/' or self.left.operator == '-'):
            term_to_move = self.left.left
            name = f"{self.right.name} {operator} {term_to_move.name}"
            self.right = Term(name, None, self.right, term_to_move, operator)
            self.right.evaluate()
            self.left = self.left.right
        else:
            term_to_move = self.left.right
            name = f"{self.right.name} {operator} {term_to_move.name}"
            self.right = Term(name, None, self.right, term_to_move, operator)
            if not term_to_move.contains_humn():
                self.right.evaluate()
            self.left = self.left.left

    def move_right_to_left(self):
        term_to_move: Term
        operator = opposite_operator(self.right.operator)
        if self.right.right.contains_humn() and not (self.right.operator == '/' or self.right.operator == '-'):
            term_to_move = self.right.left
            name = f"{self.left.name} {operator} {term_to_move.name}"
            self.left = Term(name, None, self.left, term_to_move, operator)
            self.left.evaluate()
            self.right = self.right.right
        else:
            term_to_move = self.right.right
            name = f"{self.left.name} {operator} {term_to_move.name}"
            self.left = Term(name, None, self.left, term_to_move, operator)
            if not term_to_move.contains_humn():
                self.left.evaluate()
            self.right = self.right.left

def opposite_operator(operator: str) -> str:
    if operator == '+':
        return '-'
    if operator == '-':
        return '+'
    if operator == '*':
        return '/'
    if operator == '/':
        return '*'

def evaluate(monkey: str, all_monkeys: dict):
    value = all_monkeys[monkey]
    if isinstance(value, int):
        return value
    operations = (' + ', ' - ', ' * ', ' / ')
    for operation in operations:
        if operation not in value:
            continue
        left, right = map(lambda m: evaluate(m, all_monkeys), value.split(operation))
        if operation == ' + ':
            return left + right
        elif operation == ' - ':
            return left - right
        elif operation == ' * ':
            return left * right
        else:
            return int(left / right)

def contains_humn(monkey: str, all_monkeys: dict):
    if monkey == 'humn':
        return True
    value = all_monkeys[monkey]
    if isinstance(value, int):
        return False
    left, right = re.split(' [+\-*/] ', value)
    if contains_humn(left, all_monkeys) or contains_humn(right, all_monkeys):
        return True
    return False

def build_term(monkey: str, all_monkeys: dict):
    if monkey == 'humn':
        return Term('humn')
    value = all_monkeys[monkey]
    if isinstance(value, int):
        return Term(monkey, value)
    operations = (' + ', ' - ', ' * ', ' / ')
    for operation in operations:
        if operation not in value:
            continue
        left, right = map(lambda m: build_term(m, all_monkeys), value.split(operation))
        return Term(monkey, None, left, right, operation.strip())

def evaluate_equals(all_monkeys: dict):
    value = all_monkeys['root']
    left, right = re.split(' [+\-*/] ', value)
    left_val = 0
    right_val = 0
    term: Term
    if contains_humn(left, all_monkeys):
        left_val = build_term(left, all_monkeys)
        right_val = evaluate(right, all_monkeys)
        term = Term('root', None, left_val, Term(right, right_val), '=')
    else:
        left_val = evaluate(left, all_monkeys)
        right_val = build_term(right, all_monkeys)
        term = Term('root', None, Term(left, left_val), right_val, '=')
    # Solve for humn, I guess
    term.solve()

filename = 'input-21'
monkeys = parse_input(filename)
monkeys['humn'] = 0

evaluate_equals(monkeys)