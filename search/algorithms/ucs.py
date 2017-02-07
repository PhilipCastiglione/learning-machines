"""Uniform Cost Search is a search strategy where, starting at the root of a
tree of nodes to explore, each node's children are explored in order of lowest
movement cost, with cost accumulating per move and priority given to nodes
remaining with least cost.
"""

# TODO: docs

class Node:
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent
        self.lowest_cost = cost

class Heap:
    def __init__(self):
        self.contents = []
        self.max = 0

    def insert(self, element):
        self.contents.append(element)
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    def update_costs(self, state, parent, cost):
        for node in self.contents:
            if node.state == state and node.lowest_cost > cost:
                node.lowest_cost = cost
                node.parent = parent

    def extract_min(self):
        values = [node.lowest_cost for node in self.contents]
        idx = values.index(min(values))
        return self.contents.pop(idx)

class Ucs:
    def __init__(self, subject):
        self.subject = subject
        self.frontier = Heap()
        self.explored = []
        self.success_node = None
        self.current_cost = 0

    def search(self):
        self.frontier.insert(Node(self.subject.current_state(), None, 0))

        while self.frontier.contents:
            node = self.frontier.extract_min()
            self.explored.append(node)

            self.current_cost = node.lowest_cost

            self.subject.set_state(node.state)

            if self.subject.current_state() == self.subject.goal_state():
                self.success_node = node
                return True

            self._add_next_states(node)

        return False

    """Returns statistics describing the search."""
    # TODO: update results output and document
    def results(self):
        if self.success_node:
            moves = [self.success_node]
            parent = self.success_node.parent
            while parent:
                moves.append(parent)
                parent = parent.parent
            moves.reverse()
        else:
            moves = []

        return {
            "cost": self.current_cost,
            "path": [node.state for node in moves],
            "visited_nodes": len(self._visited_nodes()),
            "frontier_nodes": len(self.frontier.contents),
            "max_frontier_nodes": self.frontier.max,
            "max_search_depth": len(moves)
        }

    def _visited_nodes(self):
        return self.explored + self.frontier.contents or []

    def _add_next_states(self, parent):
        for state in self.subject.next_states():
            cost = self.current_cost
            if [node.state for node in self._visited_nodes()].count(state) == 0:
                cost += self.subject.move_cost(self.subject.current_state(), state)
                self.frontier.insert(Node(state, parent, cost))
            elif [node.state for node in self.frontier.contents].count(state) == 1:
                cost += self.subject.move_cost(self.subject.current_state(), state)
                self.frontier.update_costs(state, parent, cost)
