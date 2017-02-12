# TODO doc
# refer: https://en.wikipedia.org/wiki/Tic-tac-toe
class TicTacToe:
    # TODO doc

    # TODO doc
    def __init__(self):
        self.board = [None] * 9
        self.dim = 3

    # TODO doc
    def move(self, index, player):
        self.board[index] = player

    # TODO doc
    def print(self):
        for row in range(self.dim):
            for col in range(self.dim):
                cell = self.board[row * 3 + col]
                if (cell == None):
                    piece = "-"
                elif (cell == 0):
                    piece = "O"
                elif (cell == 1):
                    piece = "X"
                print(piece, end=" ")
            print()
