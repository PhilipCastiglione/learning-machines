# TODO: docs

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

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

class Dfs:
    def __init__(self, subject):
        self.subject = subject
        self.frontier = Stack()
        self.explored = []
        self.success_node = None

    def search(self):
        self.frontier.push(Node(self.subject.current_state(), None))

        while self.frontier:
            node = self.frontier.pop()
            self.explored.append(node)

            self.subject.set_state(node.state)

            if self.subject.current_state() == self.subject.goal_state():
                self.success_node = node
                return True

            self._add_next_states(node)

        return False

    def results(self):
        moves = [self.success_node]
        parent = self.success_node.parent
        while parent:
            moves.append(parent)
            parent = parent.parent
        moves.reverse()

        return {
            "cost": len(moves),
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
            if [node.state for node in self._visited_nodes()].count(state) == 0:
                self.frontier.push(Node(state, parent))
