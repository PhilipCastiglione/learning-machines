# TODO: docs

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 1

class Stack:
    def __init__(self):
        self.contents = []
        self.max = 0

    def push(self, element):
        self.contents.append(element)
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    def pop(self):
        return self.contents.pop()

class Ids:
    def __init__(self, subject):
        self.subject = subject
        self.initial_state = subject.current_state()
        self.success_node = None
        self.frontier = Stack()
        self.explored = []
        self.peak_depth = 0

    def search(self, max_depth=1):
        self._reset()
        self.frontier.push(Node(self.subject.current_state(), None))

        while self.frontier.contents:
            node = self.frontier.pop()
            self.explored.append(node)
            if node.depth > self.peak_depth:
                self.peak_depth = node.depth

            self.subject.set_state(node.state)

            if self.subject.current_state() == self.subject.goal_state():
                self.success_node = node
                return True

            self._add_next_states(node, max_depth)

        if max_depth > self.peak_depth:
            return False
        else:
            return self.search(max_depth + 1)

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
            "cost": len(moves),
            "path": [node.state for node in moves],
            "visited_nodes": len(self._visited_nodes()),
            "frontier_nodes": len(self.frontier.contents),
            "max_frontier_nodes": self.frontier.max,
            "max_search_depth": len(moves)
        }

    def _reset(self):
        self.subject.set_state(self.initial_state)
        self.frontier = Stack()
        self.explored = []
        self.peak_depth = 0

    def _visited_nodes(self):
        return self.explored + self.frontier.contents or []

    def _add_next_states(self, parent, max_depth):
        for state in self.subject.next_states():
            nodes_with_state = [node.state for node in self._visited_nodes()].count(state)
            if nodes_with_state == 0 and parent.depth <= max_depth:
                self.frontier.push(Node(state, parent))
