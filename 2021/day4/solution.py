class Number:
    value: int
    marked: bool

    def __init__(self, value: int):
        self.marked = False
        self.value = value
    
    def set_marked(self):
        self.marked = True

    def set_marked_if_equal(self, value: int):
        if self.value == value:
            self.set_marked()

    def __repr__(self):
        return f"{self.value} ({'V' if self.marked else 'X'})"

class Board:
    board: list[list[Number]]
    def __init__(self, board: list[str]):
        self.board = [[] for _ in range(len(board))]
        for i, row in enumerate(board):
            for column in row.split():
                self.board[i].append(Number(int(column)))

    def mark_if_present(self, value: int):
        for row in self.board:
            for number in row:
                number.set_marked_if_equal(value)

    def calculate_score(self, number_drawn: int):
        score = 0
        for row in self.board:
            for number in row:
                if not number.marked:
                    score += number.value
        return score * number_drawn
    
    def check_if_win(self):
        needed_to_win_cols = len(self.board)
        needed_to_win_rows = len(self.board[0])
        for i in range(needed_to_win_cols):
            row_complete = 0
            col_complete = 0
            for j in range(needed_to_win_rows):
                if self.board[i][j].marked:
                    row_complete += 1
                if self.board[j][i].marked:
                    col_complete += 1
            if row_complete == needed_to_win_rows or col_complete == needed_to_win_cols:
                return True
            else:
                row_complete = 0
                col_complete = 0
        return False
    
    def __repr__(self):
        return "Board:\n" + "\n".join(["\t".join([repr(number) for number in row]) for row in self.board])
        
with open('input.txt', 'r') as f:
    first_line = f.readline()
    print(len(first_line))
    draws = [int(n) for n in first_line.split(',')]
    boards = [line.strip() for line in f.readlines() if len(line.strip()) > 0]

boards = [Board(boards[i:i+5]) for i in range(0, len(boards), 5)]
boards_won = [False for _ in range(len(boards))]

for number_drawn in draws:
    for i, board in enumerate(boards):
        board.mark_if_present(number_drawn)
        win = board.check_if_win()
        if win:
            boards_won[i] = True
            if all(boards_won):
                print(board.calculate_score(number_drawn))
                exit()
