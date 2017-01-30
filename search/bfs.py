# TODO: docs

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

class Queue:
    def __init__(self):
        self.contents = []
        self.max = 0

    def enqueue(self, element):
        self.contents.insert(0, element)
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    def dequeue(self):
        return self.contents.pop()

class Bfs:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.frontier = Queue()
        self.explored = []
        self.success_node = None

    def success(self):
        return self.state_machine.current_state() == self.state_machine.goal_state()

    def visited_nodes(self):
        return self.explored + self.frontier.contents or []

    def add_next_states(self, parent):
        for state in self.state_machine.next_states():
            if [node.state for node in self.visited_nodes()].count(state) == 0:
                self.frontier.enqueue(Node(state, parent))

    def search(self):
        self.frontier.enqueue(Node(self.state_machine.current_state(), None))

        while self.frontier:
            node = self.frontier.dequeue()
            self.explored.append(node)

            self.state_machine.set_state(node.state)

            if self.success():
                self.success_node = node
                return True

            self.add_next_states(node)

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
            "visited_nodes": len(self.visited_nodes()),
            "frontier_nodes": len(self.frontier.contents),
            "max_frontier_nodes": self.frontier.max,
            "max_search_depth": len(moves)
        }
