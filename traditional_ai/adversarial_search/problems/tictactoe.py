import os

# TODO doc
# refer: https://en.wikipedia.org/wiki/Tic-tac-toe
class TicTacToe:
    # TODO doc

    # TODO doc
    def __init__(self):
        self.board = [None] * 9
        self.current_player = None

    # TODO doc
    def print(self):
        os.system(["clear","cls"][os.name == "nt"])
        for row in range(3):
            for col in range(3):
                cell = self.board[row * 3 + col]
                piece = {
                    None: "-",
                    0: "O",
                    1: "X"
                }[cell]
                print(piece, end=" ")
            print()

    # TODO doc
    def player_move(self):
        prompt = "Enter row and column of move (like this: 11): "
        valid_moves = ["1","2","3"]
        valid_move = False
        while (valid_move == False):
            input_move = input(prompt)
            if (input_move[0] in valid_moves and input_move[1] in valid_moves):
                move = (int(input_move[0]) - 1) * 3 + int(input_move[1]) - 1
                if (self.board[move] == None):
                    valid_move = True
        self.board[index] = 0

    # TODO doc
    def winner(self, state=self.board):
        if (state[0] == state[1] == state[2] != None):
            return state[0]
        elif (state[3] == state[4] == state[5] != None):
            return state[3]
        elif (state[6] == state[7] == state[8] != None):
            return state[6]
        elif (state[0] == state[3] == state[6] != None):
            return state[0]
        elif (state[1] == state[4] == state[7] != None):
            return state[1]
        elif (state[2] == state[5] == state[8] != None):
            return state[2]
        elif (state[0] == state[4] == state[8] != None):
            return state[0]
        elif (state[2] == state[4] == state[6] != None):
            return state[2]
        elif (state.count(None) == 0):
            return 2 # This is a draw condition
        return None # There is no winner yet

    # TODO doc
    def set_state(self, state):
        self.board = state

    # TODO doc
    def curent_state(self):
        return self.board

    # TODO doc
    def next_states(self):
        pass # TODO
