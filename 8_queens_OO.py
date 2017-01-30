import time

class Cell:
    """A Cell is a square on the chessboard, which might contain a queen. A Cell
    knows where it is on the Board, it's current state, and can interact with
    the Board through queening.
    """
    def __init__(self, idx, board):
        self.idx = idx
        self.board = board
        self.row = idx // 8 + 1
        self.col = idx % 8 + 1
        self.is_queen = False
        self.is_attacked = False

    """The cell has a queen on it, and the Board updates newly attacked cells.
    """
    def queen(self):
        self.is_queen = True
        self.board.calculate_attacked(self)

    """The cell no longer has a queen on it, and the Board recalculates all
    attacked cells.
    """
    def unqueen(self):
        self.is_queen = False
        self.board.calculate_all_attacked()

class Board:
    """The Board manages the state of it's Cells and provides methods for
    calculating which cells are currently attacked, and which cells a queen
    that is placed will be able to attack.
    """
    def __init__(self):
        self.cells = [Cell(i, self) for i in range(64)]

    def reset(self):
        for cell in self.cells:
            cell.is_queen = False
            cell.is_attacked = False

    """For debugging purposes."""
    def display(self):
        for r in range(8):
            for c in range(8):
                cell = self.cells[r * 8 + c]
                if cell.is_queen:
                    print(" [Q]", end=" ")
                else:
                    print(" {:2} ".format(cell.idx), end=" ")
            print()

    """Queens a cell, if it is legal to do so given the rules."""
    def attempt_queening(self, cell_idx):
        cell = self.cells[cell_idx]
        if cell.is_attacked == False:
            cell.queen()

    """The current queens on the board."""
    def queens(self):
        queens = []
        for cell in self.cells:
            if cell.is_queen:
                queens += [cell]
        return queens

    """Sets newly attacked cells for a placed queen."""
    def calculate_attacked(self, cell):
        for c in self.attackable_cells(cell):
            c.is_attacked = True

    """Calculates all attacked cells based on the current queen set."""
    def calculate_all_attacked(self):
        for cell in self.cells:
            cell.is_attacked = False
        for queen in self.queens():
            self.calculate_attacked(queen)

    """Determines which cells are attackable from the position of a Cell."""
    def attackable_cells(self, cell):
        cells = []
        cells.extend(self.cells_in_dir(cell, self.nw_cell))
        cells.extend(self.cells_in_dir(cell, self.n_cell))
        cells.extend(self.cells_in_dir(cell, self.ne_cell))
        cells.extend(self.cells_in_dir(cell, self.w_cell))
        cells.extend(self.cells_in_dir(cell, self.e_cell))
        cells.extend(self.cells_in_dir(cell, self.sw_cell))
        cells.extend(self.cells_in_dir(cell, self.s_cell))
        cells.extend(self.cells_in_dir(cell, self.se_cell))
        return cells

    """Recursively determines and adds cells in a given direction until the edge
    of the board is reached.
    """
    def cells_in_dir(self, cell, dir, acc_cells=[]):
        next_cell = dir(cell)
        if next_cell is not None:
            return self.cells_in_dir(next_cell, dir, acc_cells + [next_cell])
        else:
            return acc_cells

    def nw_cell(self, cell):
        if cell.row > 1 and cell.col > 1:
            return self.cells[cell.idx - 9]

    def n_cell(self, cell):
        if cell.row > 1:
            return self.cells[cell.idx - 8]

    def ne_cell(self, cell):
        if cell.row > 1 and cell.col < 8:
            return self.cells[cell.idx - 7]

    def w_cell(self, cell):
        if cell.col > 1:
            return self.cells[cell.idx - 1]

    def e_cell(self, cell):
        if cell.col < 8:
            return self.cells[cell.idx + 1]

    def sw_cell(self, cell):
        if cell.row < 8 and cell.col > 1:
            return self.cells[cell.idx + 7]

    def s_cell(self, cell):
        if cell.row < 8:
            return self.cells[cell.idx + 8]

    def se_cell(self, cell):
        if cell.row < 8 and cell.col < 8:
            return self.cells[cell.idx + 9]

class Engine:
    """Engine connects the elements of the environment required to execute a
    strategy to solve the 8 queens problem.
    """
    def __init__(self, board):
        self.board = board
        self.solutions = []

    def reset(self):
        self.board.reset()
        self.solutions = []

    """Result output."""
    def output_solutions(self, time):
        print("Found {} solutions in {:.2f} seconds:".format(len(self.solutions), time))

    """Runs a strategy in a clean environment and provides output."""
    def run(self, strategy):
        self.reset()
        print("using: {}".format(strategy.__name__))
        t = time.time()
        strategy(board, self.solutions)
        self.output_solutions(time.time() - t)

class Strategy:
    """Strategy contains different search strategies that can be used to find
    solutions to the 8 queens problem.
    """

    """Checks the goal state and if achieved, adds the current state to the
    solution set."""
    def check_and_add_solution(self, queens, solutions):
        if len(queens) == 8:
            solutions.append([queen.idx for queen in queens])

    """A strategy where each each cell is inspected linearly for queening,
    queened if possible, then when all legal queens have been placed a board
    configuration is examined for success. Then, the last placed queen is
    backtracked and the next cell after that cell is inspected."""
    def linear_backtrack(self, board, solutions):
        cell_idx = 0
        starting_cell_idx = 0
        # There must be a queen in the first row
        while starting_cell_idx < 8:
            board.attempt_queening(cell_idx)
            # if we're at the end of a run
            if cell_idx == 63:
                self.check_and_add_solution(board.queens(), solutions)
                cell_idx, starting_cell_idx = self.backtrack(cell_idx, starting_cell_idx, board.queens())
            cell_idx += 1

    """Backtrack the last placed queen (or two if required) and return the
    indices of the current cell under examination and the starting cell for the
    next run through of the board."""
    def backtrack(self, cell_idx, starting_cell_idx, queens):
        queens[-1].unqueen()

        # if there was only one queen, progress to next run
        if len(queens) == 1:
            return starting_cell_idx, starting_cell_idx + 1

        # if the last queen was on an end cell
        elif queens[-1].idx == 63:
            # unqueen the second last queen
            queens[-2].unqueen()
            # if there are no queens left, progress to next run
            if len(queens) == 2:
                return starting_cell_idx, starting_cell_idx + 1
            # otherwise, continue the run from the second last queen
            else:
                return queens[-2].idx, starting_cell_idx

        # otherwise, continue the run from the last queen
        else:
            return queens[-1].idx, starting_cell_idx

    """A strategy where every board combination is generated then inspected,
    with the limitation that we can only place a single queen in any row or
    column, which we know is required because of problem domain knowledge."""
    def brute_force(self, board, solutions):
        for q1 in range(8):
            for q2 in set(range(8)) - { q1 }:
                for q3 in set(range(8)) - { q1, q2 }:
                    for q4 in set(range(8)) - { q1, q2, q3 }:
                        for q5 in set(range(8)) - { q1, q2, q3, q4 }:
                            for q6 in set(range(8)) - { q1, q2, q3, q4, q5 }:
                                for q7 in set(range(8)) - { q1, q2, q3, q4, q5, q6 }:
                                    for q8 in set(range(8)) - { q1, q2, q3, q4, q5, q6, q7 }:
                                        board.reset()
                                        board.attempt_queening(q1 + 0 * 8)
                                        board.attempt_queening(q2 + 1 * 8)
                                        board.attempt_queening(q3 + 2 * 8)
                                        board.attempt_queening(q4 + 3 * 8)
                                        board.attempt_queening(q5 + 4 * 8)
                                        board.attempt_queening(q6 + 5 * 8)
                                        board.attempt_queening(q7 + 6 * 8)
                                        board.attempt_queening(q8 + 7 * 8)
                                        self.check_and_add_solution(board.queens(), solutions)

# Establish state and run each strategy with output
if __name__ == '__main__':
    board = Board()
    engine = Engine(board)
    strategy = Strategy()

    engine.run(strategy.brute_force)
    engine.run(strategy.linear_backtrack)
