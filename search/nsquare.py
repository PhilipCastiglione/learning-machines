import math

class Board:
    def __init__(self, tile_nums):
        self.dim = int(math.sqrt(len(tile_nums) + 1))
        self.tiles = []
        for num in tile_nums:
            self.tiles.append(num)

    def empty_cell(self):
        return self.tiles.index(0)

    def print_board(self):
        for i in range(self.dim):
            for j in range(self.dim):
                print(self.tiles[i * self.dim + j], end=" ")
            print()

p = [1,2,5,3,4,0,6,7,8]
b = Board(p)
b.print_board()
print(b.empty_cell())
