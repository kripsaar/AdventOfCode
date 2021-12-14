rules = {}
char_count = {}

def parse_input(filename: str):
    global rules
    with open(filename, mode="r") as input:
        polymer, rules = [half.strip() for half in input.read().split("\n\n")]
        rules = [line.strip().split(" -> ") for line in rules.split("\n")]
        rules = {line[0]: line[1] for line in rules}
        for char in polymer:
            if char not in char_count:
                char_count[char] = 0
            char_count[char] += 1
    return polymer

def step(polymer: str):
    global rules
    global char_count
    new_polymer = ""
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        insert = ""
        if pair in rules:
            insert = rules[pair]
            if insert not in char_count:
                char_count[insert] = 0
            char_count[insert] += 1
        new_polymer += pair[0] + insert
    new_polymer += polymer[-1]
    return new_polymer

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


polymer = parse_input("input-14")

for i in range(10):
    polymer = step(polymer)
calc_score()
