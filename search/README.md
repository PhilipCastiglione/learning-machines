# Search
Search is a common problem in computer science and artificial intelligence. Here
we have a number of common search algorithms demonstrated.

## Algorithms
1. Breadth-First Search (`bfs.py`)
1. Depth-First Search (`dfs.py`)
1. Limited Depth Search (`lds.py`)
1. Iterative Deepening Search (`ids.py`)

## Problem Domain
A problem is required as the domain in which to test the search algorithms.

I am using the [n-puzzle](https://en.wikipedia.org/wiki/15_puzzle) problem because
it is _"a classical problem for modelling algorithms involving heuristics"_.

I am further using TODO (something for UCS, A star, IDA star)

## Running
TODO:
        print("USAGE")
        print("available search algos include: {}".format(list(algos.keys())))
        print("initial board state must be a valid n-square board input as a csv (no spaces)")
        print("example:")
        print("    python3 driver.py bfs 1,2,3,0,5,6,4,7,8")
        exit(2)

## TODO
1. Documentation
1. Finish README
1. make the output more reasonable and specific to the algo

## TODO ALGOS
1. Problem type with non 1 step cost
1. Uniform-Cost Search (`ucs.py`)
1. Greedy Best-First Search (`gbfs.py`)
1. A\*/A-Star (`astar.py`)
1. IDA\*/IDA-Star (`idastar.py`)
1. Dijkstra's Algorithm (`dijkstra.py`)
