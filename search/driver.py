# TODO: docs
import sys
import time
import resource

from problems.npuzzle import Npuzzle
from problems.travel import Travel

from algorithms.bfs import Bfs
from algorithms.dfs import Dfs
from algorithms.lds import Lds
from algorithms.ids import Ids
from algorithms.ucs import Ucs

def handle_input():
    algos = {
        "bfs": Bfs, # Breadth-First Search
        "dfs": Dfs, # Depth-First Search
        "lds": Lds, # Limited Depth Search
        "ids": Ids, # Iterative Deepening Search
        "ucs": Ucs  # Uniform-Cost Search
    }

    problems = {
        "npuzzle": Npuzzle,
        "travel": Travel,
    }

    state_decoders = {
        "npuzzle": lambda x: [int(n) for n in x.split(",")],
        "travel": lambda x: x
    }

    if len(sys.argv) != 4:
        print("Invalid usage. Please refer to README.md")
        exit(2)
    else:
        return algos[sys.argv[1]], problems[sys.argv[2]], state_decoders[sys.argv[2]](sys.argv[3])

def run(strategy):
    start_time = time.time()
    # TODO is memory working?
    memory = resource.getrusage(resource.RUSAGE_CHILDREN)[2]
    strategy.search()
    write_out(strategy.results(), start_time, memory)

def write_out(results, start_time, memory):
    output_file = open("./output.txt", "w")

    results["time"] = time.time() - start_time
    results["memory"] = memory

    for field in results:
        output_file.write("{}: {}\n".format(field, results[field]))

    output_file.close()
    print("Search completed. Results in output.txt")

if __name__ == '__main__':
    algorithm, puzzle, initial_state = handle_input()

    strategy = algorithm(puzzle(initial_state))

    run(strategy)
