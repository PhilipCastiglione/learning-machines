"""Greedy Best-First Search is a search strategy where, starting at the root of
a tree of nodes to explore, the visible children are explored in turn with
priority given to the node with the lowest heuristic score.
"""

class Node:
    """A node represents a particular point in search space, contained within
    the tree of state spaces to search for a goal state.
    """

    """Instantiate with a state representation, a link to a parent node and a
    cost.
    """
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent # for reconstructing success path
        self.cost = cost

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

    """Remove and return the item with lowest current cost from the Heap."""
    def extract_min(self):
        values = [node.cost for node in self.contents]
        idx = values.index(min(values))
        return self.contents.pop(idx)

class Gbfs:
    """This class implements the Greedy Best-First Search strategy."""

    """Instantiate with a subject to search, an empty Heap to store nodes
    currently on the frontier of search space, an empty array to store nodes
    that have been explored, and a variable to store a node with the goal state.
    """
    def __init__(self, subject):
        self.subject = subject
        self.frontier = Heap()
        self.explored = []
        self.success_node = None # for reconstructing success path

    """Executes the search strategy and returns a boolean indicating success."""
    def search(self):
        # add the initial state to the Heap
        initial_state = self.subject.current_state()
        initial_cost = self.subject.heuristic_cost()
        self.frontier.insert(Node(initial_state, None, initial_cost))

        while self.frontier.contents:
            # remove the next item from the Heap and explore it
            node = self.frontier.extract_min()
            self.explored.append(node)

            self.subject.set_state(node.state)

            # if the node we are exploring matches the goal state, we are done
            if self.subject.current_state() == self.subject.goal_state():
                self.success_node = node
                return True

            # otherwise finish exploring the node by adding it's next states to
            # the frontier
            self._add_next_states(node)

        # if we have explored every node and not found the solution, we are done
        return False

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

        return {
            "path": [(node.state, self.subject.heuristic_cost(node.state)) for node in path],
            "path length": len(path),
            "number of visited nodes": len(self._visited_nodes()),
            "current frontier nodes": [(node.state, node.cost) for node in self.frontier.contents],
            "number of frontier nodes": len(self.frontier.contents),
            "max number of frontier nodes": self.frontier.max
        }

    """Visited nodes includes explored nodes and nodes on the frontier."""
    def _visited_nodes(self):
        return self.explored + self.frontier.contents or [] # must return a list

    """Adds states that can be reached from the current state to the Heap."""
    def _add_next_states(self, parent):
        for state in self.subject.next_states():
            # only add states that have never been visited
            if [node.state for node in self._visited_nodes()].count(state) == 0:
                cost = self.subject.heuristic_cost(state)
                self.frontier.insert(Node(state, parent, cost))
