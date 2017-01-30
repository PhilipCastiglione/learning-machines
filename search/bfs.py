# TODO: docs

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.on_frontier = False
        self.explored = False

class Bfs:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.frontier = []

    def success(self):
        return self.state_machine.current_state() == self.state_machine.goal_state()

    def search(self):
        if self.success():
            # TODO: starting in winning position
            return True

        initial_state = Node(self.state_machine.current_state(), None)
        initial_state.explored = True

        self.frontier = initial_state.next_states()

        while self.frontier:
            pass

        # bail when we get a success
        # while the frontier isn't empty...
        # explore according to breath
        # if the frontier is empty and we never got success
        # then bail because we failed
        pass

    def results(self):
        pass
