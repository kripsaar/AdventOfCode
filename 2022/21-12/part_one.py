

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
            return left / right

filename = 'input-21'
monkeys = parse_input(filename)

result = evaluate('root', monkeys)
print(int(result))