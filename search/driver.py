import sys
import time
import resource

import nsquare
import bfs

def handle_input():
    algos = {"bfs": bfs.Bfs}

    if len(sys.argv) != 3:
        print("required args include the search algo and the initial board state")
        print("available search algos include: {}".format(list(algos.keys())))
        print("initial board state must be a valid n-square board or crazy stuff may occur")
        print("initial board state must be a CSV string with no spaces")
        print("example:")
        print("    python3 driver.py bfs 1,2,3,0,5,6,4,7,8")
        exit(2)
    else:
        return algos[sys.argv[1]], [int(n) for n in sys.argv[2].split(",")]

if __name__ == '__main__':
    algorithm, initial_state = handle_input()

    strategy = algorithm(nsquare.Board(initial_state))

    start_time = time.time()
    result = strategy.search()

    output_file = open("./output.txt", "w")
    if result:
        results = strategy.results()
        results["time"] = time.time() - start_time
        # TODO is memory working?
        results["memory"] = resource.getrusage(resource.RUSAGE_CHILDREN)[2]
        # TODO:
        print(results)
        # spit out results to file
    else:
        # TODO:
        print("No solution found!")
        # spit out this message to file along with stats
