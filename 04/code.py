from collections import defaultdict

SIZE = 5


class Board:
    def __init__(self, data):
        self.data = data
        self.mark_map = [[0 for i in range(SIZE)] for j in range(SIZE)]
        self.win = False

    def mark(self, row, column):
        if self.mark_map[row][column] == 1:
            return

        self.mark_map[row][column] = 1

        # update win
        if sum(self.mark_map[row]) == SIZE:
            self.win = True
            return

        marks_in_column = [self.mark_map[row][column] for row in range(SIZE)]
        if sum(marks_in_column) == SIZE:
            self.win = True
            return   

    def getScore(self):
        score = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if self.mark_map[i][j] == 0:
                    score += self.data[i][j]
        return score


with open('input') as f:
    numbers = map(int, f.readline().strip().split(','))
    boards =[]
    data = []
    number_map = defaultdict(list)
    line = f.readline()
    while line:
        row_data = line.strip()
        if not row_data:
            if data:
                boards.append(Board(data))
                data = []
        else:
            row = list(map(int, row_data.split()))
            for i in range(SIZE):
                value = row[i]
                number_map[value].append((len(boards), len(data), i))
            data.append(row)
        line = f.readline()

    first_winner = None
    last_winner = None
    boards_remain = set(range(len(boards)))
    for n in numbers:
        changes = number_map[n]
        for index, row, column in changes:
            board = boards[index]
            if not board.win:
                board.mark(row, column)
                if board.win:
                    if not first_winner:
                        first_winner = (n, board)
                    boards_remain.discard(index)
                    if len(boards_remain) == 0:
                        last_winner = (n, board)
                        break
        else:
            continue
        break
    

    print('part one answer: {}'.format(first_winner[0] * first_winner[1].getScore()))
    print('part two answer: {}'.format(last_winner[0] * last_winner[1].getScore()))