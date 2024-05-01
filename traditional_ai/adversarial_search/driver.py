"""Driver sets up the algorithm and problem space, sets up an interactive loop
for user input and provides output.
"""
import sys
import time
import resource # TODO
import random

#from algorithms.bfs import Bfs
from problems.tictactoe import TicTacToe

"""Handle user input and return the selected algorithm and problem."""
def handle_input():
    algorithms = {
        #"bfs": Bfs, # Breadth-First Search
    }

    problems = {
        "tictactoe": TicTacToe,
    }

    if len(sys.argv) != 3:
        print("Invalid usage. Please refer to README.md")
        exit(2)
    else:
        #return algorithms[sys.argv[1]], problems[sys.argv[2]]
        return None, problems[sys.argv[2]]

# TODO doc
def play(puzzle, strategy):
    start(puzzle)
    while (puzzle.winner() == None):
        next_turn(puzzle, strategy)
    end(puzzle)

# TODO doc
def start(puzzle):
    puzzle.print()
    puzzle.current_player = random.randint(0, 1)
    if (puzzle.current_player == 0):
        print("You go first!")
    else:
        print("The AI will go first.")
    time.sleep(2)

# TODO doc
def next_turn(puzzle, strategy):
    puzzle.print()
    if (puzzle.current_player == 0):
        puzzle.player_move()
    else:
        puzzle.set_state(strategy.search())
    puzzle.current_player = 1 - puzzle.current_player

# TODO doc
def end(puzzle):
    puzzle.print()
    if (puzzle.winner() == 0):
        print("Congratulations, you win!")
    elif (puzzle.winner() == 1):
        print("The AI has won.")
    else:
        print("The game is a draw.")

"""Write the results out to a file."""
def write_out(results):
    output_file = open("./output.txt", "w")

    keys = list(results.keys())
    keys.sort()

    for field in keys:
        format_string = {
            int: "{}: {:,}\n",
            float: "{}: {:2f}\n",
            str: "{}: {}\n",
            list: "{}: {}\n"
        }[type(results[field])]
        output_file.write(format_string.format(field, results[field]))

    output_file.close()
    print("Process completed. Results in output.txt")

"""Set up the game with the strategy and play until complete, then report."""
if __name__ == '__main__':
    algorithm, puzzle = handle_input()
    
    game = puzzle()
    strategy = algorithm(game)

    play(game, strategy)

    write_out(strategy.results())
