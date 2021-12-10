import math

start = ['(', '[', '{', '<']
end = [')', ']', '}', '>']
match_dict = {')' : '(', ']' : '[', '}' : '{', '>' : '<', '(' : ')', '[' : ']', '{' : '}', '<' : '>'}
point_dict = {')' : 1, ']' : 2, '}' : 3, '>' : 4}

def score_completion_string(completion_string: list):
    score = 0
    for char in completion_string:
        score = (score * 5) + point_dict[char]
    return score


def evaluate_line(line: str):
    open_chunks = []
    for char in line:
        if char in start:
            open_chunks.append(char)
            continue
        if match_dict[char] != open_chunks.pop():
            return 0
    completion_string = []
    for index in range(len(open_chunks)):
        char = open_chunks.pop()
        new_char = match_dict[char]
        line += new_char
        completion_string.append(new_char)
    return score_completion_string(completion_string)
    
def calc_final_score(scores: list):
    scores.sort()
    return scores[math.floor(len(scores) / 2)]
        
filename = "input-10"

scores = []
with open(filename, mode="r") as input:
    for line in input:
        score = evaluate_line(line.strip())
        if score > 0:
            scores.append(score)

score = calc_final_score(scores)

print(f"Score: {score}")