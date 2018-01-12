# NOTE: there are too many combinations to calculate board states but we CAN
# calculate all the states for the 8 cells that are the factors of a cells next
# cell state (similarly for edge and corner cells).

import itertools

# this is run once code so it doesn't need to be efficient or nice sorry
class StatesGenerator:
    def __init__(self):
        self.top_left = {}
        self.top_right = {}
        self.bottom_left = {}
        self.bottom_right = {}
        self.top = {}
        self.bottom = {}
        self.left = {}
        self.right = {}
        self.middle = {}

    def generate(self):
        for cell_type in [self.top_left, self.top_right, self.bottom_left, self.bottom_right]:
            for c in itertools.product('.01', repeat=4):
                key = ''.join(c)
                value = self.next_state(cell_type, key)
                cell_type[key] = value

        for cell_type in [self.top, self.bottom, self.left, self.right]:
            for c in itertools.product('.01', repeat=6):
                key = ''.join(c)
                value = self.next_state(cell_type, key)
                cell_type[key] = value

        for c in itertools.product('.01', repeat=9):
            key = ''.join(c)
            value = self.next_state(cell_type, key)
            self.middle[key] = value

    def next_state(self, cell_type, state):
        if cell_type == self.top_left:
            neighbour_state = state[1:]
            current_cell = state[0]
        elif cell_type == self.top_right:
            neighbour_state = state[0] + state[2:]
            current_cell = state[1]
        elif cell_type == self.bottom_left:
            neighbour_state = state[0:2] + state[3]
            current_cell = state[2]
        elif cell_type == self.bottom_right:
            neighbour_state = state[0:3]
            current_cell = state[3]
        elif cell_type == self.top:
            neighbour_state = state[0] + state[2:]
            current_cell = state[1]
        elif cell_type == self.bottom:
            neighbour_state = state[0:4] + state[5]
            current_cell = state[4]
        elif cell_type == self.left:
            neighbour_state = state[0:2] + state[3:]
            current_cell = state[2]
        elif cell_type == self.right:
            neighbour_state = state[0:3] + state[4:]
            current_cell = state[3]
        elif cell_type == self.middle:
            neighbour_state = state[0:4] + state[5:]
            current_cell = state[4]

        stats = self.get_stats(neighbour_state)
        count = stats['count']
        if (count == 2 or count == 3) and current_cell != '.':
            next_state = current_cell
        elif count == 3:
            next_state = stats['majority']
        else:
            next_state = '.'

        return next_state

    def get_stats(self, state):
        stats = {}
        stats['count'] = len(state) - state.count('.')
        if state.count('1') > state.count('0'):
            stats['majority'] = '1'
        else:
            stats['majority'] = '0'
        return stats

    def output(self):
        print('top_left = {}'.format(self.top_left))
        print('top_right = {}'.format(self.top_right))
        print('bottom_left = {}'.format(self.bottom_left))
        print('bottom_right = {}'.format(self.bottom_right))
        print('top = {}'.format(self.top))
        print('bottom = {}'.format(self.bottom))
        print('left = {}'.format(self.left))
        print('right = {}'.format(self.right))
        print('middle = {}'.format(self.middle))

sg = StatesGenerator()
sg.generate()
sg.output()
