rules = {}
char_count = {}

def add_pair(pair: str, pairs: dict, count: int = 1):
    if pair not in pairs:
        pairs[pair] = 0
    pairs[pair] += count

def increment_char_count(char: str, count: int = 1):
    global char_count
    if char not in char_count:
        char_count[char] = 0
    char_count[char] += count


def extract_pairs(polymer):
    pairs = {}
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        add_pair(pair, pairs)
    return pairs

def parse_input(filename: str):
    global rules
    with open(filename, mode="r") as input:
        polymer, rules = [half.strip() for half in input.read().split("\n\n")]
        rules = [line.strip().split(" -> ") for line in rules.split("\n")]
        rules = {line[0]: line[1] for line in rules}
        for char in polymer:
            increment_char_count(char)
    return extract_pairs(polymer)

def step(pairs: dict):
    global rules
    global char_count
    new_pairs = {}

    for pair in pairs:
        if pair not in rules:
            add_pair(pair, new_pairs)
            continue
        count = pairs[pair]
        insert = rules[pair]
        increment_char_count(insert, count)
        add_pair(pair[0] + insert, new_pairs, count)
        add_pair(insert + pair[1], new_pairs, count)
    return new_pairs

def calc_score():
    global char_count
    most_common = max(char_count, key=char_count.get)
    least_common = min(char_count, key=char_count.get)
    most_common_value = char_count[most_common]
    least_common_value = char_count[least_common]
    score = most_common_value - least_common_value
    print(f"Most common char is {most_common} with {most_common_value} occurances")
    print(f"Least common char is {least_common} with {least_common_value} occurances")
    print()
    print(f"Score = {score}")


pairs = parse_input("input-14")

for i in range(40):
    pairs = step(pairs)
calc_score()
