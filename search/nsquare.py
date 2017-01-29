import math

class Tile:
    def __init__(self, board, number):
        self.board = board
        self.number = number

class Board:
    def __init__(self, tile_nums):
        self.dim = int(math.sqrt(len(tile_nums) + 1))
        self.empty_cell = None
        self.cells = []
        self.setup_board(tile_nums)

    def setup_board(self, tile_nums):
        for i, tile in enumerate(tile_nums):
            if tile == 0:
                self.empty_cell = i
                self.cells.append(None)
            else:
                self.cells.append(Tile(self, tile))

    def print_board(self):
        output = []
        for tile in self.cells:
            if tile:
                output.append(tile.number)
            else:
                output.append(" ")
        for i in range(self.dim):
            for j in range(self.dim):
                print(output[i * self.dim + j], end=" ")
            print()

p = [1,2,5,3,4,0,6,7,8]
b = Board(p)
b.print_board()
print(b.empty_cell)
