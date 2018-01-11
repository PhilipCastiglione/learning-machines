# NOTE: there are too many combinations to calculate
# we can calculate perhaps just the combinations for a known non replacement scenario
# such as 188 * '.' 50 * '1' and 50 * '0'
# this might provide a shortcut for the start of the game

from itertools import combinations_with_replacement

# test state and next state
# s = '.,.,.,.,.,0,0,.,.,.,.,.,.,1,.,1,.,.,.,.,.,.,.,.,0,0,.,0,.,.,.,.,.,1,.,.,.,.,1,.,.,.,.,.,.,.,.,0,.,.,1,1,1,.,1,.,.,.,1,.,1,1,.,.,.,.,.,.,0,.,1,.,1,.,.,.,.,.,1,.,.,.,1,.,1,0,1,.,.,0,.,0,.,.,0,.,.,.,1,.,.,.,1,.,.,.,1,.,1,.,.,0,0,.,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,1,0,0,0,.,.,.,.,0,.,.,.,0,.,0,.,.,.,1,.,.,0,.,1,1,.,.,.,1,0,.,0,.,.,.,0,.,.,1,.,.,0,0,.,.,1,.,.,.,.,.,.,.,.,.,1,1,.,1,0,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,.,1,.,.,0,.,.,.,.,.,0,.,.,.,.,.,.,.,.,.,1,.,.,.,0,.,0,1,0,.,0,.,.,0,0,.,.,.,1,.,1,.,1,.,1,.,.,.,.,.,.,0,0,0,.,.,.,.,0,.,.,.,.,.,.,1,.,.,.,.,.,.,.,.,0,.,.,0,.'
# n = '.,.,.,.,.,0,0,0,.,.,.,.,.,.,1,.,.,.,.,.,.,.,.,0,0,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,.,.,0,.,.,.,.,.,1,.,1,.,.,1,.,.,.,1,1,1,.,.,.,1,0,.,.,.,1,1,1,1,.,.,.,.,1,.,.,.,.,1,1,.,1,.,1,0,1,0,.,0,0,.,.,1,.,.,.,1,1,.,.,.,.,.,.,.,.,0,.,.,0,.,0,.,.,.,.,.,.,.,.,.,.,.,.,0,.,.,.,.,0,0,.,.,.,.,.,.,0,.,.,.,.,.,.,.,.,.,0,.,1,1,0,.,1,1,0,.,.,.,.,.,.,1,.,1,.,.,.,.,0,.,.,1,.,.,.,.,.,.,.,.,1,1,1,1,.,.,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,1,.,1,.,.,.,.,.,.,.,.,0,0,.,.,.,.,0,.,.,1,1,.,.,.,.,.,0,.,0,0,.,.,.,0,.,0,.,.,.,.,.,.,.,.,1,.,1,0,.,.,.,0,.,0,.,.,.,.,0,.,.,.,.,.,.,.,.,.,.,.,0,.,.,.,.,.,.,.,.'
class StatesGenerator:
    @classmethod
    def generate(cls):
        results = {}
        for c in combinations_with_replacement('.01', 288):
            s = cls(','.join(c))
            key = s.serialize_state()
            s.set_next_state()
            s.state = s.next_state
            value = s.serialize_state()
            results[key] = value
        print(results)

    def __init__(self, state):
        self.state = []
        self.next_state = []

        state_list = state.split(',')
        self.rows = 16
        self.columns = 18

        for r in range(self.rows):
            self.next_state.append([])
            row = []
            for c in range(self.columns):
                self.next_state[r].append([])
                row.append(state_list[self.columns * r + c])
            self.state.append(row)

    def serialize_state(self):
        flat_list = []
        for row in self.state:
            flat_list.extend(row)
        return ','.join(flat_list)

    def print_state(self):
        for row in self.state:
            print(' '.join(row))

    def set_next_state(self):
        for r in range(self.rows):
            for c in range(self.columns):
                neighbours = self.get_neighbours(r, c)
                if neighbours['count'] == 2 and self.is_alive(r, c):
                    next_c = self.state[r][c]
                elif neighbours['count'] == 3:
                    if self.is_alive(r, c):
                        next_c = self.state[r][c]
                    else:
                        next_c = neighbours['majority']
                else:
                    next_c = '.'
                self.next_state[r][c] = next_c

    def get_neighbours(self, r, c):
        neighbours = {}
        neighbour_cells = []

        if r == 0 and c == 0:
            neighbour_cells.append(self.state[0][1])
            neighbour_cells.append(self.state[1][0])
            neighbour_cells.append(self.state[1][1])
        elif r == 0 and c == 17:
            neighbour_cells.append(self.state[0][16])
            neighbour_cells.append(self.state[1][16])
            neighbour_cells.append(self.state[1][17])
        elif r == 15 and c == 0:
            neighbour_cells.append(self.state[14][0])
            neighbour_cells.append(self.state[14][1])
            neighbour_cells.append(self.state[15][1])
        elif r == 15 and c == 17:
            neighbour_cells.append(self.state[14][16])
            neighbour_cells.append(self.state[14][17])
            neighbour_cells.append(self.state[15][16])
        else:
            if r == 0:
                neighbour_cells.append(self.state[0][c - 1])
                neighbour_cells.append(self.state[0][c + 1])
                neighbour_cells.append(self.state[1][c - 1])
                neighbour_cells.append(self.state[1][c - 0])
                neighbour_cells.append(self.state[1][c + 1])
            elif r == 15:
                neighbour_cells.append(self.state[15][c - 1])
                neighbour_cells.append(self.state[15][c + 1])
                neighbour_cells.append(self.state[14][c - 1])
                neighbour_cells.append(self.state[14][c - 0])
                neighbour_cells.append(self.state[14][c + 1])
            elif c == 0:
                neighbour_cells.append(self.state[r - 1][0])
                neighbour_cells.append(self.state[r + 1][0])
                neighbour_cells.append(self.state[r - 1][1])
                neighbour_cells.append(self.state[r - 0][1])
                neighbour_cells.append(self.state[r + 1][1])
            elif c == 17:
                neighbour_cells.append(self.state[r - 1][17])
                neighbour_cells.append(self.state[r + 1][17])
                neighbour_cells.append(self.state[r - 1][16])
                neighbour_cells.append(self.state[r - 0][16])
                neighbour_cells.append(self.state[r + 1][16])
            else:
                neighbour_cells.append(self.state[r - 1][c - 1])
                neighbour_cells.append(self.state[r - 1][c - 0])
                neighbour_cells.append(self.state[r - 1][c + 1])
                neighbour_cells.append(self.state[r - 0][c - 1])
                # neighbour_cells.append(self.state[r - 0][c - 0])
                neighbour_cells.append(self.state[r - 0][c + 1])
                neighbour_cells.append(self.state[r + 1][c - 1])
                neighbour_cells.append(self.state[r + 1][c - 0])
                neighbour_cells.append(self.state[r + 1][c + 1])

        neighbours['count'] = len(neighbour_cells) - neighbour_cells.count('.')
        if neighbour_cells.count('1') > neighbour_cells.count('0'):
            neighbours['majority'] = '1'
        else:
            neighbours['majority'] = '0'
        return neighbours

    def is_alive(self, r, c):
        return self.state[r][c] != '.'

StatesGenerator.generate()
