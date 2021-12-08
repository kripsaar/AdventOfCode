def parse_input(filename: str):
    result = []
    with open(filename, mode="r") as input:
        for line in input:
            line = [["".join(sorted(item)) for item in half.strip().split(" ")] for half in line.split("|")]
            result.append(line)
    return result

def solve_a(one, seven):
    for char in seven:
        if char not in one:
            return char

def solve_three(one, twothreefive):
    one_set = set([char for char in one])
    for candidate in twothreefive:
        candidate_set = set([char for char in candidate])
        if one_set.issubset(candidate_set):
            return candidate

def solve_nine(four, zerosixnine):
    four_set = set([char for char in four])
    for candidate in zerosixnine:
        candidate_set = set([char for char in candidate])
        if four_set.issubset(candidate_set):
            return candidate

def solve_zero_six(one, zerosix):
    one_set = set([char for char in one])
    zero = ""
    for candidate in zerosix:
        candidate_set = set([char for char in candidate])
        if one_set.issubset(candidate_set):
            zero = candidate
    zerosix.remove(zero)
    six = zerosix[0]
    return {0 : zero, 6 : six}

def solve_two_five(nine, twofive):
    nine_set = set([char for char in nine])
    five = ""
    for candidate in twofive:
        candidate_set = set([char for char in candidate])
        if candidate_set.issubset(nine_set):
            five = candidate
    twofive.remove(five)
    two = twofive[0]
    return {5 : five, 2 : two}


def solve_digits(observed: list):
    digits = {}
    reverse_digits = {}
    for item in observed:
        if len(item) == 2:
            digits[1] = item
        elif len(item) == 3:
            digits[7] = item
        elif len(item) == 4:
            digits[4] = item
        elif len(item) == 7:
            digits[8] = item
    digits[3] = solve_three(digits[1], list(filter(lambda x: len(x) == 5, observed)))
    digits[9] = solve_nine(digits[4], list(filter(lambda x: len(x) == 6, observed)))
    
    zerosix_candidates = list(filter(lambda x: len(x) == 6, observed))
    zerosix_candidates.remove(digits[9])
    zerosix = solve_zero_six(digits[1], zerosix_candidates)
    digits = {**digits, **zerosix}

    twofive_candidates = list(filter(lambda x: len(x) == 5, observed))
    twofive_candidates.remove(digits[3])
    twofive = solve_two_five(digits[9], twofive_candidates)
    digits = {**digits, **twofive}

    for key, value in digits.items():
        reverse_digits[value] = key

    return reverse_digits
    
def calc_output_value(output, digits):
    res = ""
    for digit in output:
        res = res + str(digits[digit])
    return int(res)


input = parse_input("input-08")
result = 0
for observed, output in input:
    digits = solve_digits(observed)
    result += calc_output_value(output, digits)

print(result)