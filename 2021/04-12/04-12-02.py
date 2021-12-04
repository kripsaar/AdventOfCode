
class BingoBoard:
    def __init__(self, board_input):
        self.board_matrix = self.parse_board(board_input)
        self.marked_numbers = []
        self.unmarked_numbers = [number for row in self.board_matrix for number in row]
        self.last_marked = 0

    def parse_board(self, board_input):
        return [[int(item.strip()) for item in line.strip().replace("  ", " ").split(" ")] for line in board_input.splitlines()]

    def get_score(self):
        return self.last_marked * sum(self.unmarked_numbers)

    def mark(self, marked_number):
        if marked_number in self.unmarked_numbers:
            self.marked_numbers.append(marked_number)
            self.unmarked_numbers.remove(marked_number)
            self.last_marked = marked_number
    
    def is_solved(self):
        return self.check_rows() or self.check_columns()

    def check_rows(self):
        for row in self.board_matrix:
            if all(item in self.marked_numbers for item in row):
                return True

    def check_columns(self):
        column_count = len(self.board_matrix[0])
        columns = [[row[index]  for row in self.board_matrix] for index in range(column_count)]
        for column in columns:
            if all(item in self.marked_numbers for item in column):
                return True

    def print_board(self):
        for row in self.board_matrix:
            self.print_row(row)

    def print_row(self, row):
        row = [(str(item) + ("x" if item in self.marked_numbers else " ")).rjust(3) for item in row]
        print(' '.join(row))


def play(boards, input):
    winning_score = 0
    boards_temp = boards.copy()
    for mark in input:
        for board in boards:
            board.mark(mark)
            if board.is_solved():
                winning_score = board.get_score()
                print(board.print_board())
                print(board.marked_numbers)
                print(f"Last marked: {board.last_marked}")
                print(f"Score: {winning_score}")
                boards_temp.remove(board)
        boards = boards_temp.copy()
    return winning_score

input = []
boards = []
with open("input-04", mode='r') as input:
    input = input.read().split("\n\n")
    boards = [BingoBoard(board) for board in input[1:]]
    input = [int(element) for element in input[0].split(",")]

play(boards, input)