"""Breadth-First Search is a search strategy where, starting at the root of a
tree of nodes to explore, each node's children are explored in turn, with
priority given to nodes closest to the root.
"""

class Node:
    """A node represents a particular point in search space, contained within
    the tree of state spaces to search for a goal state.
    """

    """Instantiate with a state representation and a link to a parent node."""
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent # for reconstructing success path

class Queue:
    """A Queue data structure is used to order nodes to search, prioritising
    nodes added earliest, which are closest to the root node. This results in
    exploration of a tree in order of breadth first.
    """

    """Instantiate with empty contents and a maximum reached size of zero."""
    def __init__(self):
        self.contents = []
        self.max = 0 # output statistic, not used in search

    """Add an item to the end of the Queue."""
    def enqueue(self, element):
        self.contents.insert(0, element)
        # If the Queue is the longest it has been, update max.
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    """Remove and return an item from the front of the Queue."""
    def dequeue(self):
        return self.contents.pop()

class Bfs:
    """This class implements the Breadth-First Search strategy."""

    """Instantiate with a subject to search, an empty Queue to store nodes
    currently on the frontier of search space, an empty array to store nodes
    that have been explored, and a variable to store a node with the goal state.
    """
    def __init__(self, subject):
        self.subject = subject
        self.frontier = Queue()
        self.explored = []
        self.success_node = None # for reconstructing success path

    """Executes the search strategy and returns a boolean indicating success."""
    def search(self):
        # add the initial state to the Queue
        self.frontier.enqueue(Node(self.subject.current_state(), None))

        while self.frontier.contents:
            # remove the next item from the Queue and explore it
            node = self.frontier.dequeue()
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
            "path": [node.state for node in path],
            "path length/search depth": len(path),
            "number of visited nodes": len(self._visited_nodes()),
            "current frontier nodes": [node.state for node in self.frontier.contents],
            "number of frontier nodes": len(self.frontier.contents),
            "max number of frontier nodes": self.frontier.max
        }

    """Visited nodes includes explored nodes and nodes on the frontier."""
    def _visited_nodes(self):
        return self.explored + self.frontier.contents or [] # must return a list

    """Adds states that can be reached from the current state to the Queue."""
    def _add_next_states(self, parent):
        for state in self.subject.next_states():
            # only add states that have never been visited
            if [node.state for node in self._visited_nodes()].count(state) == 0:
                self.frontier.enqueue(Node(state, parent))
