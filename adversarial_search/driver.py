"""Driver sets up the algorithm and problem space, sets up an interactive loop
for user input and provides output.
"""
import sys
import time
import resource

#from algorithms.bfs import Bfs
#from problems.npuzzle import Npuzzle

"""Handle user input and return the selected algorithm and problem."""
def handle_input():
    algorithms = {
        #"bfs": Bfs, # Breadth-First Search
    }

    problems = {
        #"npuzzle": Npuzzle,
    }

    if len(sys.argv) != 3:
        print("Invalid usage. Please refer to README.md")
        exit(2)
    else:
        return algorithms[sys.argv[1]], problems[sys.argv[2]]

"""Execute the search strategy using an interactive loop for user input, then
return a results hash for output.
"""
def execute(strategy):
    # TODO
    pass

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

"""Executes the search strategy on the problem."""
if __name__ == '__main__':
    algorithm, puzzle = handle_input()

    strategy = algorithm(puzzle())

    results = execute(strategy)

    write_out(results)
