
def read_input(filename: str):
    with open(filename, mode='r') as file:
        return file.readlines()

score_map = { 'A X' : 4, 'A Y' : 8, 'A Z' : 3, 'B X' : 1, 'B Y' : 5, 'B Z' : 9, 'C X' : 7, 'C Y' : 2, 'C Z' : 6 }

filename = "input-02"
score = 0
for line in read_input(filename):
    score += score_map[line.strip()]
print(score)