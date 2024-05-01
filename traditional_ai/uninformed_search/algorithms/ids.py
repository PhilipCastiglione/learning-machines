"""Iterative Deepening Search is a variation on Depth-First Search, where the
maximum searchable depth is limited to a number, but then when that number is
reached, the number is incremented and the search is rerun. Functionality is
like Depth-First Search, though the effect in terms of finding the outcome
has similarities with Breadth-First Search, through the iterative deepening of
the depth limit. Memory usage will be optimal relative to Breadth First Search,
but there is some speed overhead with throwing away failed searches for too
shallow a depth limit.
"""

class Node:
    """A node represents a particular point in search space, contained within
    the tree of state spaces to search for a goal state.
    """

    """Instantiate with a state representation, a link to a parent node and
    calculate it's depth in the tree.
    """
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent # for reconstructing success path
        if parent: # a node with no parent has a depth of 1
            self.depth = parent.depth + 1
        else:
            self.depth = 1

class Stack:
    """A Stack data structure is used to order nodes to search, prioritising
    nodes added last, which are farthest from the root node. This results in
    exploration of a tree in order of depth first.
    """

    """Instantiate with empty contents and a maximum reached size of zero."""
    def __init__(self):
        self.contents = []
        self.max = 0 # output statistic, not used in search

    """Add an item to the top of the Stack."""
    def push(self, element):
        self.contents.append(element)
        # If the Stack is the longest it has been, update max.
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    """Remove and return an item from the top of the Stack."""
    def pop(self):
        return self.contents.pop()

class Ids:
    """This class implements the Iterative Deepening (Depth-First) Search
    strategy.
    """

    """Instantiate with a subject to search, an empty Stack to store nodes
    currently on the frontier of search space, an empty array to store nodes
    that have been explored, and a variable to store a node with the goal state.

    For this iterative version we also store the initial state, so we can return
    to it, and the peak depth visited, which we use to recognise when to reset
    and run again with an iteratively increased depth limit.
    """
    def __init__(self, subject):
        self.subject = subject
        self.initial_state = subject.current_state()
        self.success_node = None # for reconstructing success path
        self.frontier = Stack()
        self.explored = []
        self.peak_depth = 0
        self.iterations = 0 # output statistic, not used in search

    """Recursively executes the search strategy and returns a boolean indicating
    success. Max depth begins at 1 and increases with each run.
    """
    def search(self, max_depth=1):
        # at the start of a run, reset state and increment iteration count
        self._reset()
        self.iterations += 1
        # add the initial state to the Stack
        self.frontier.push(Node(self.subject.current_state(), None))

        while self.frontier.contents:
            # remove the top item from the Stack and explore it
            node = self.frontier.pop()
            self.explored.append(node)

            # increment peak depth if necessary
            if node.depth > self.peak_depth:
                self.peak_depth = node.depth

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

        return {
            "path": [node.state for node in path],
            "path length": len(path),
            "visited_nodes": len(self._visited_nodes()),
            "number of visited nodes": len(self._visited_nodes()),
            "iterations": self.iterations,
            "current frontier nodes": [node.state for node in self.frontier.contents],
            "number of frontier nodes": len(self.frontier.contents),
            "max number of frontier nodes": self.frontier.max
        }

    """Resets state to the initial state, ready for a search run."""
    def _reset(self):
        self.subject.set_state(self.initial_state)
        self.frontier = Stack()
        self.explored = []
        self.peak_depth = 0

    """Visited nodes includes explored nodes and nodes on the frontier."""
    def _visited_nodes(self):
        return self.explored + self.frontier.contents or [] # must return a list

    """Adds states that can be reached from the current state to the Stack, up
    to the present depth limit.
    """
    def _add_next_states(self, parent, max_depth):
        for state in self.subject.next_states():
            nodes_with_state = [node.state for node in self._visited_nodes()].count(state)
            # only add states that have never been visited and that are within
            # the present depth limit
            if nodes_with_state == 0 and parent.depth <= max_depth:
                self.frontier.push(Node(state, parent))
