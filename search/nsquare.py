# TODO
# an optimal algo would really just pass around the state as simple flat arrays
# need a ruleset contained in board but the data should be simples
import math

class Board:
    def __init__(self, initial_state):
        self.dim = int(math.sqrt(len(initial_state) + 1))
        self.tiles = []
        for num in initial_state:
            self.tiles.append(num)

    def print_board(self):
        for i in range(self.dim):
            for j in range(self.dim):
                print("{:2} ".format(self.tiles[i * self.dim + j]), end=" ")
            print()

    def current_state(self):
        return self.tiles

    def moves(self):
        moves = []
        empty = self.tiles.index(0)
        north = empty - self.dim
        east = empty + 1
        south = empty + self.dim
        west = empty - 1
        if north >= 0:
            moves.append(north)
        if east % self.dim != 0:
            moves.append(east)
        if south < self.dim * self.dim:
            moves.append(south)
        if west & self.dim != 1:
            moves.append(west)
        return moves

    def state_for_move(self, tile_idx):
        tiles = self.tiles.copy()
        tiles[self.tiles.index(0)] = tiles[tile_idx]
        tiles[tile_idx] = 0
        return tiles

    def next_states(self):
        states = []
        for move in self.moves():
            states.append(self.state_for_move(move))
        return states

    def set_state(self, state):
        self.tiles = state

p1 = [1,2,5,3,4,0,6,7,8]
b1 = Board(p1)
print("initial state")
b1.print_board()
print("possible next states:")
for state in b1.next_states():
    b1.set_state(state)
    b1.print_board()
    print("---------")

p2 = [6,8,11,0,7,2,15,12,3,10,4,5,9,13,14,1]
b2 = Board(p2)
b2.print_board()
print("possible next states:")
for state in b2.next_states():
    b2.set_state(state)
    b2.print_board()
    print("---------")
