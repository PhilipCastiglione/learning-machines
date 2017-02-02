import math

class Board:
    """Board defines the shape, contents and rules for the n-square puzzle
    board, and makes itself available as a state machine for search algorithms.
    """

    """Instantiate with an initial state and cache dimensions."""
    def __init__(self, initial_state):
        self.dim = int(math.sqrt(len(initial_state) + 1))
        self.tiles = initial_state

    """For debugging."""
    def print(self):
        for i in range(self.dim):
            for j in range(self.dim):
                print("{:2} ".format(self.tiles[i * self.dim + j]), end=" ")
            print()

    """Returns the current state."""
    def current_state(self):
        return self.tiles

    """Returns the cost of moving from one state to another state. The move
    is assumed to be legal.
    """
    def move_cost(self, state1, state2):
        # given that the move must be legal, the cost is always 1 in n-puzzle
        return 1

    """Returns the cost of the current state, determined using the Manhattan
    Distance heuristic, or rectilinear distance.
    """
    def heuristic_cost(self):
        cost = 0
        for current_idx, tile in enumerate(self.tiles):
            if tile != 0:
                goal_idx = tile - 1
                # add the distance in rows
                cost += abs(goal_idx // self.dim - current_idx // self.dim)
                # add the distance in columns
                cost += abs(goal_idx % self.dim - current_idx % self.dim)
        return cost

    """Returns the legal states available from the current state."""
    def next_states(self):
        states = []
        for move in self._moves():
            states.append(self._state_for_move(move))
        return states

    """Sets the current state."""
    def set_state(self, state):
        self.tiles = state

    """Returns the goal state."""
    def goal_state(self):
        state = list(range(len(self.tiles)))
        state.remove(0)
        state.append(0)
        return state

    """Calculate and return the indices of legal moves."""
    def _moves(self):
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

    """Calculate and return the state associated with a legal move."""
    def _state_for_move(self, tile_idx):
        tiles = self.tiles.copy()
        tiles[self.tiles.index(0)] = tiles[tile_idx]
        tiles[tile_idx] = 0
        return tiles
