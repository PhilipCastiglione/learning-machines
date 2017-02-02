# TODO: docs
import sys
import time
import resource

import npuzzle
import bfs
import dfs
import dfsl
import idfs

def handle_input():
    algos = {
        "bfs": bfs.Bfs,    # Breadth First Search
        "dfs": dfs.Dfs,    # Depth First Search
        "dfsl": dfsl.Dfsl, # Depth-Limited Depth First Search
        "idfs": idfs.Idfs  # Iterative Deepening Depth First Search
    }

    if len(sys.argv) != 3:
        print("USAGE")
        print("available search algos include: {}".format(list(algos.keys())))
        print("initial board state must be a valid n-square board input as a csv (no spaces)")
        print("example:")
        print("    python3 driver.py bfs 1,2,3,0,5,6,4,7,8")
        exit(2)
    else:
        return algos[sys.argv[1]], [int(n) for n in sys.argv[2].split(",")]

def write_out(results, start_time):
    output_file = open("./output.txt", "w")

    results["time"] = time.time() - start_time
    # TODO is memory working?
    results["memory"] = resource.getrusage(resource.RUSAGE_CHILDREN)[2]

    # TODO: fix output of results approach
    if results.get("path"):
        output_file.write("Solution found:\n")
        output_file.write("time: {:.2f} seconds\n".format(results["time"]))
        output_file.write("memory: {:,.2f}KB\n".format(results["memory"]))
        output_file.write("cost: {}\n".format(results["cost"]))
        output_file.write("max_search_depth: {}\n".format(results["max_search_depth"]))
        output_file.write("path: {}\n".format(results["path"]))
    else:
        output_file.write("No solution found!\n")

    output_file.write("visited_nodes: {}\n".format(results["visited_nodes"]))
    output_file.write("frontier_nodes: {}\n".format(results["frontier_nodes"]))
    output_file.write("max_frontier_nodes: {}\n".format(results["max_frontier_nodes"]))
    output_file.close()
    print("Search completed. Results in output.txt")

if __name__ == '__main__':
    algorithm, initial_state = handle_input()

    strategy = algorithm(npuzzle.Board(initial_state))

    start_time = time.time()
    strategy.search()
    write_out(strategy.results(), start_time)
