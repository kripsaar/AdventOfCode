
def read_input(filename: str):
    with open(filename, mode='r') as file:
        return file.readlines()
# A = Rock = 1
# B = Paper = 2
# C = Scissors = 3

# X = lose = 0
# Y = draw = 3
# Z = win = 6
score_map = { 'A X' : 0 + 3, 'A Y' : 3 + 1, 'A Z' : 6 + 2, 'B X' : 1, 'B Y' : 3 + 2, 'B Z' : 6 + 3, 'C X' : 0 + 2, 'C Y' : 3 + 3, 'C Z' : 6 + 1 }

filename = "input-02"
score = 0
for line in read_input(filename):
    score += score_map[line.strip()]
print(score)