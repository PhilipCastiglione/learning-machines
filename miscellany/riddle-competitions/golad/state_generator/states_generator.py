# NOTE: there are too many combinations to calculate board states
# but we CAN calculate all the states for the 8 cells that are the
# factors of a cells next cell state

import itertools

class StatesGenerator:
    @classmethod
    def generate(cls):
        # corner cells
        corner_cells = {}
        for c in itertools.product('.01', repeat=3):
            key = ''.join(c)
            value = cls.next_state(key)
            corner_cells[key] = value
        print(corner_cells)
        # edge cells
        edge_cells = {}
        for c in itertools.product('.01', repeat=5):
            key = ''.join(c)
            value = cls.next_state(key)
            edge_cells[key] = value
        print(edge_cells)
        # non edge cells
        full_cells = {}
        for c in itertools.product('.01', repeat=8):
            key = ''.join(c)
            value = cls.next_state(key)
            full_cells[key] = value
        print(full_cells)

    @staticmethod
    def next_state(state):
        neighbours = {}
        neighbours['count'] = len(state) - state.count('.')
        if state.count('1') > state.count('0'):
            neighbours['majority'] = '1'
        else:
            neighbours['majority'] = '0'
        return neighbours

StatesGenerator.generate()
