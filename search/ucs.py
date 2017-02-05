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
        # TODO: need to update any connected nodes with
        # lower costs
        if len(self.contents) > self.max:
            self.max = len(self.contents)

    def extract_min(self):
        values = [node.lowest_cost for nodes in self.contents]
        idx = values.index(min(values))
        return self.contents.pop(idx)

class Ucs:
    def __init__(self, subject):
        self.subject = subject
        self.frontier = Heap()
        self.explored = []
        self.success_node = None

    def search(self):
        pass # TODO

    def results(self):
        pass # TODO

    def _visited_nodes(self):
        return self.explored + self.frontier.contents or []

    def _add_next_states(self, parent):
        pass # TODO
