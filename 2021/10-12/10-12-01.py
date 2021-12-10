start = ['(', '[', '{', '<']
end = [')', ']', '}', '>']
match_dict = {')' : '(', ']' : '[', '}' : '{', '>' : '<'}
point_dict = {')' : 3, ']' : 57, '}' : 1197, '>' : 25137}


def evaluate_line(line: str):
    open_chunks = []
    for char in line:
        if char in start:
            open_chunks.append(char)
            continue
        if match_dict[char] != open_chunks.pop():
            return point_dict[char]
    return 0
        
filename = "input-10"

score = 0
with open(filename, mode="r") as input:
    for line in input:
        score += evaluate_line(line.strip())

print(f"Score: {score}")