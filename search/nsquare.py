# TODO: docs
import math

class Board:
    def __init__(self, initial_state):
        self.dim = int(math.sqrt(len(initial_state) + 1))
        self.tiles = []
        for num in initial_state:
            self.tiles.append(num)

    def print(self):
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

    def goal_state(self):
        state = list(range(len(self.tiles)))
        state.remove(0)
        state.append(0)
        return state
