"""A-Star (A*) Search is a search strategy where, starting at the root of a tree 
of nodes to explore, each node's children are explored in order of a combination
of lowest movement cost, with cost accumulating per move and a heuristic cost.
Priority of exploration is given to those remaining with lowest combined cost.
"""

class Node:
    """A node represents a particular point in search space, contained within
    the tree of state spaces to search for a goal state.
    """

    """Instantiate with a state representation, a link to a parent node. the
    heuristic cost associated with the node's state and a record of the lowest
    movement cost to reach that node currently found.
    """
    def __init__(self, state, parent, movement_cost, heuristic_cost):
        self.state = state
        self.parent = parent
        self.movement_cost = movement_cost
        self.heuristic_cost = heuristic_cost

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
        self.max = 0

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

class Astar:
    """This class implements the A-Star (A*) Search strategy."""

    """Instantiate with a subject to search, an empty Heap to store nodes
    currently on the frontier of search space, an empty array to store nodes
    that have been explored, the current movement cost of state for accumulation
    and a variable to store a node with the goal state.
    """
    def __init__(self, subject):
        self.subject = subject
        self.frontier = Heap()
        self.explored = []
        self.success_node = None
        self.current_cost = 0

    """Executes the search strategy and returns a boolean indicating success."""
    def search(self):
        # add the initial state to the Heap
        initial_state = self.subject.current_state()
        initial_cost = self.subject.heuristic_cost()
        self.frontier.insert(Node(initial_state, None, 0, initial_cost))

        while self.frontier.contents:
            # remove the next item from the Heap and explore it
            node = self.frontier.extract_min()
            self.explored.append(node)

            # update the current cost for accumulation to children states
            self.current_cost = node.movement_cost

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

        costs = lambda x: (x.state, x.movement_cost, x.heuristic_cost, x.cost())

        return {
            "cost": self.current_cost,
            "path": [costs(node) for node in path],
            "path length": len(path),
            "number of visited nodes": len(self._visited_nodes()),
            "current frontier nodes": [costs(node) for node in self.frontier.contents],
            "number of frontier nodes": len(self.frontier.contents),
            "max number of frontier nodes": self.frontier.max
        }

    """Visited nodes includes explored nodes and nodes on the frontier."""
    def _visited_nodes(self):
        return self.explored + self.frontier.contents or [] # must return a list

    """Adds states that can be reached from the current state to the Heap."""
    def _add_next_states(self, parent):
        for state in self.subject.next_states():
            movement_cost = self.current_cost
            # only add states that have never been visited
            if [node.state for node in self._visited_nodes()].count(state) == 0:
                movement_cost += self.subject.move_cost(self.subject.current_state(), state)
                heuristic_cost = self.subject.heuristic_cost(state)
                self.frontier.insert(Node(state, parent, movement_cost, heuristic_cost))
            # though also check to update the cost of any state we can now reach
            # at lower cost
            elif [node.state for node in self.frontier.contents].count(state) == 1:
                movement_cost += self.subject.move_cost(self.subject.current_state(), state)
                self.frontier.update_costs(state, parent, movement_cost)
