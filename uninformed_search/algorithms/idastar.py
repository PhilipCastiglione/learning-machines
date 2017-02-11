"""IDA-Star (A*) Search is a variation on A-Star where the maximum searchable
depth is limited to a number, which is incrementally increased when the limited
depth tree is exhausted of possibilities.

Functionally IDA-Star is like A-Star but with the speed overhead associated with
failure runs where the limit was too low to contain the solution, but with lower
memory usage.
"""

class Node:
    """A node represents a particular point in search space, contained within
    the tree of state spaces to search for a goal state.
    """

    """Instantiate with a state representation, a link to a parent node. the
    heuristic cost associated with the node's state, a record of the lowest
    movement cost to reach that node currently found and it's depth.
    """
    def __init__(self, state, parent, movement_cost, heuristic_cost):
        self.state = state
        self.parent = parent # for reconstructing success path
        self.movement_cost = movement_cost
        self.heuristic_cost = heuristic_cost
        if parent: # a node with no parent has a depth of 1
            self.depth = parent.depth + 1
        else:
            self.depth = 1

    """Returns the total cost associated with the node."""
    def cost(self):
        return self.movement_cost + self.heuristic_cost

class Heap:
    """A Heap (or Priority Queue) is used to order nodes to search, prioritising
    nodes with minimum current cost for extraction.
    """

    """Instantiate with empty contents and a maximum reached size of zero."""
    def __init__(self):
        self.contents = []
        self.max = 0 # output statistic, not used in search

    """Add an item to the Heap."""
    def insert(self, element):
        self.contents.append(element)
        # If the Heap is the largest it has been, update max.
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    """Update the cost of any node which is found to have a cheaper movement cost
    to reach, and update that node's parent also.
    """
    def update_costs(self, state, parent, movement_cost):
        for node in self.contents:
            if node.state == state and node.movement_cost > movement_cost:
                node.movement_cost = movement_cost
                node.parent = parent

    """Remove and return the item with lowest current cost from the Heap."""
    def extract_min(self):
        values = [node.cost() for node in self.contents]
        idx = values.index(min(values))
        return self.contents.pop(idx)

class Idastar:
    """This class implements the IDA-Star (IDA*) Search strategy."""

    """Instantiate with a subject to search, an empty Heap to store nodes
    currently on the frontier of search space, an empty array to store nodes
    that have been explored, the current movement cost of state for accumulation
    and a variable to store a node with the goal state.

    For this iterative version we also store the initial state, so we can return
    to it, and the peak depth visited, which we use to recognise when to reset
    and run again with an iteratively increased depth limit.
    """
    def __init__(self, subject):
        self.subject = subject
        self.initial_state = subject.current_state()
        self.success_node = None # for reconstructing success path
        self.frontier = Heap()
        self.explored = []
        self.current_cost = 0
        self.peak_depth = 0
        self.iterations = 0 # output statistic, not used in search

    """Recursively executes the search strategy and returns a boolean indicating
    success. Max depth begins at 1 and increases with each run.
    """
    def search(self, max_depth=1):
        # at the start of a run, reset state and increment iteration count
        self._reset()
        self.iterations += 1
        # add the initial state to the Heap
        initial_state = self.subject.current_state()
        initial_cost = self.subject.heuristic_cost()
        self.frontier.insert(Node(initial_state, None, 0, initial_cost))

        while self.frontier.contents:
            # remove the next item from the Heap and explore it
            node = self.frontier.extract_min()
            self.explored.append(node)

            # increment peak depth if necessary
            if node.depth > self.peak_depth:
                self.peak_depth = node.depth

            # update the current cost for accumulation to children states
            self.current_cost = node.movement_cost

            self.subject.set_state(node.state)

            # if the node we are exploring matches the goal state, we are done
            if self.subject.current_state() == self.subject.goal_state():
                self.success_node = node
                return True

            # otherwise finish exploring the node by adding it's next states to
            # the frontier
            self._add_next_states(node, max_depth)

        # if we have explored every node and the depth limit exceeds our peak
        # depth, there is no solution and we are done
        if max_depth > self.peak_depth:
            return False
        else:
            # otherwise, increase max depth and recurse
            return self.search(max_depth + 1)

    """Returns statistics describing the search."""
    def results(self):
        if self.success_node:
            # construct the success path
            path = [self.success_node]
            parent = self.success_node.parent
            while parent:
                path.append(parent)
                parent = parent.parent
            path.reverse()
        else:
            path = []

        costs = lambda x: (x.state, x.movement_cost, x.heuristic_cost, x.cost())

        return {
            "cost": self.current_cost,
            "path": [costs(node) for node in path],
            "path length": len(path),
            "number of visited nodes": len(self._visited_nodes()),
            "iterations": self.iterations,
            "current frontier nodes": [costs(node) for node in self.frontier.contents],
            "number of frontier nodes": len(self.frontier.contents),
            "max number of frontier nodes": self.frontier.max
        }

    """Resets state to the initial state, ready for a search run."""
    def _reset(self):
        self.subject.set_state(self.initial_state)
        self.frontier = Heap()
        self.explored = []
        self.peak_depth = 0
        self.current_cost = 0

    """Visited nodes includes explored nodes and nodes on the frontier."""
    def _visited_nodes(self):
        return self.explored + self.frontier.contents or [] # must return a list

    """Adds states that can be reached from the current state to the Heap."""
    def _add_next_states(self, parent, max_depth):
        for state in self.subject.next_states():
            movement_cost = self.current_cost
            nodes_with_state = [node.state for node in self._visited_nodes()].count(state)
            # only add states that have never been visited and that are within
            # the present depth limit
            if nodes_with_state == 0 and parent.depth <= max_depth:
                movement_cost += self.subject.move_cost(self.subject.current_state(), state)
                heuristic_cost = self.subject.heuristic_cost(state)
                self.frontier.insert(Node(state, parent, movement_cost, heuristic_cost))
            # though also check to update the cost of any state we can now reach
            # at lower cost
            elif [node.state for node in self.frontier.contents].count(state) == 1:
                movement_cost += self.subject.move_cost(self.subject.current_state(), state)
                self.frontier.update_costs(state, parent, movement_cost)
