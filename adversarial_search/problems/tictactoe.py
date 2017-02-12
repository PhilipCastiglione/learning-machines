import random
import os
import time

# TODO doc
# refer: https://en.wikipedia.org/wiki/Tic-tac-toe
class TicTacToe:
    # TODO doc

    # TODO doc
    def __init__(self):
        self.board = [None] * 9
        self.current_player = None

    # TODO doc
    def play(self):
        self._start()
        while (self._winner() == None):
            self._next_turn()
        self._end()

    # TODO doc
    def _start(self):
        self._print()
        self.current_player = random.randint(0, 1)
        if (self.current_player == 0):
            print("You go first!")
        else:
            print("The AI will go first.")
        time.sleep(2)

    # TODO doc
    def _print(self):
        os.system(["clear","cls"][os.name == "nt"])
        for row in range(3):
            for col in range(3):
                cell = self.board[row * 3 + col]
                if (cell == None):
                    piece = "-"
                elif (cell == 0):
                    piece = "O"
                elif (cell == 1):
                    piece = "X"
                print(piece, end=" ")
            print()

    # TODO doc
    def _next_turn(self):
        self._print()
        if (self.current_player == 0):
            self._player_move()
        else:
            self._ai_move()
        self.current_player = 1 - self.current_player

    # TODO doc
    def _player_move(self):
        prompt = "Enter row and column of move (like this: 11): "
        valid_moves = ["1","2","3"]
        valid_move = False
        while (valid_move == False):
            input_move = input(prompt)
            if (input_move[0] in valid_moves and input_move[1] in valid_moves):
                move = (int(input_move[0]) - 1) * 3 + int(input_move[1]) - 1
                if (self.board[move] == None):
                    valid_move = True
        self._move(move, 0)

    # TODO doc
    def _ai_move(self):
        # temporary testing
        self._move(int(input("ai move is an index: ")), 1)

    # TODO doc
    def _move(self, index, player):
        self.board[index] = player

    # TODO doc
    def _winner(self):
        cells = self.board
        if (cells[0] == cells[1] == cells[2] != None):
            return cells[0]
        elif (cells[3] == cells[4] == cells[5] != None):
            return cells[3]
        elif (cells[6] == cells[7] == cells[8] != None):
            return cells[6]
        elif (cells[0] == cells[3] == cells[6] != None):
            return cells[0]
        elif (cells[1] == cells[4] == cells[7] != None):
            return cells[1]
        elif (cells[2] == cells[5] == cells[8] != None):
            return cells[2]
        elif (cells[0] == cells[4] == cells[8] != None):
            return cells[0]
        elif (cells[2] == cells[4] == cells[6] != None):
            return cells[2]
        elif (cells.count(None) == 0):
            return 2 # This is a draw condition
        return None # There is no winner yet

    # TODO doc
    def _end(self):
        self._print()
        if (self._winner() == 0):
            print("Congratulations, you win!")
        elif (self._winner() == 1):
            print("The AI has won.")
        else:
            print("The game is a draw.")
