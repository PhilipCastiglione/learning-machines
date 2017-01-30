import sys

import nsquare
#import bfs.Bfs as bfs

# TODO: put things in a main function and so on
algos = {"bfs": None}#bfs}

if len(sys.argv) != 3:
    print("required args include the search algo and the initial board state")
    print("available search algos include: {}".format(list(algos.keys())))
    print("initial board state must be a valid n-square board or crazy stuff may occur")
    print("initial board state must be a CSV string with no spaces")
    print("example:")
    print("    python3 driver.py bfs 1,2,5,3,4,0,6,7,8")
    exit(2)
else:
    algo = algos[sys.argv[1]]
    initial_state = sys.argv[2].split(",")

# TODO: do the search yo
output_file = open("./output.txt", "w")

board = nsquare.Board(initial_state)
strategy = algo(board)

result = strategy.search()
if result:
    results = strategy.results()
    # TODO:
    # spit out results to file
else:
    # TODO:
    print("No solution found!")
    # spit out this message to file along with stats

# TODO: output for file
'''
path_to_goal: the sequence of moves taken to reach the goal
cost_of_path: the number of moves taken to reach the goal
nodes_expanded: the number of nodes that have been expanded
fringe_size: the size of the frontier set when the goal node is found
max_fringe_size: the maximum size of the frontier set in the lifetime of the algorithm
search_depth: the depth within the search tree when the goal node is found
max_search_depth:  the maximum depth of the search tree in the lifetime of the algorithm
running_time: the total running time of the search instance, reported in seconds
max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes
'''

