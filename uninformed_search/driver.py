"""Driver coordinates input, the running of an algorithm on a problem and
produces output.
"""
import sys
import time
import resource

from algorithms.bfs import Bfs
from algorithms.dfs import Dfs
from algorithms.lds import Lds
from algorithms.ids import Ids
from algorithms.ucs import Ucs
from algorithms.gbfs import Gbfs
from algorithms.astar import Astar
from algorithms.idastar import Idastar
from problems.npuzzle import Npuzzle
from problems.travel import Travel

"""Interpret the input from the user and return the algorithm, puzzle and
decoded state input.
"""
def handle_input():
    algorithms = {
        "bfs": Bfs, # Breadth-First Search
        "dfs": Dfs, # Depth-First Search
        "lds": Lds, # Limited Depth Search
        "ids": Ids, # Iterative Deepening Search
        "ucs": Ucs, # Uniform-Cost Search
        "gbfs": Gbfs, # Greedy Best-First Search
        "astar": Astar, # A-Star/A* Search
        "idastar": Idastar # A-Star/A* Search
    }

    problems = {
        "npuzzle": Npuzzle,
        "travel": Travel,
    }

    state_decoders = {
        "npuzzle": lambda x: [int(n) for n in x.split(",")],
        "travel": lambda x: x.lower()
    }

    if len(sys.argv) != 4:
        print("Invalid usage. Please refer to README.md")
        exit(2)
    else:
        return algorithms[sys.argv[1]], problems[sys.argv[2]], state_decoders[sys.argv[2]](sys.argv[3])

"""Execute the search strategy and record some additional metrics, return the
results hash for output.
"""
def run(strategy):
    start_time = time.time()

    strategy.search()
    results = strategy.results()

    results["time (s)"] = time.time() - start_time
    results["memory (kb)"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    return results

"""Write the results out to a file."""
def write_out(results):
    keys = list(results.keys())
    keys.sort()

    format_strings = {
        int: "{}: {:,}\n",
        float: "{}: {:2f}\n",
        str: "{}: {}\n",
        list: "{}: {}\n"
    }

    with open("./output.txt", mode="w", encoding="utf-8") as output_file:
        for field in keys:
            format_string = format_strings[type(results[field])]
            output_file.write(format_string.format(field, results[field]))

    print("Search completed. Results in output.txt")

"""Executes the search strategy on the problem with the provided state."""
if __name__ == '__main__':
    algorithm, puzzle, initial_state = handle_input()

    strategy = algorithm(puzzle(initial_state))

    results = run(strategy)

    write_out(results)
