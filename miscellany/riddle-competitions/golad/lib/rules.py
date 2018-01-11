import settings


class Rules:
    @classmethod
    def calculate_next_state(cls, state):
        next_state = ''
        for row in range(settings.ROWS):
            for col in range(settings.COLUMNS):
                neighbours = cls._get_neighbours(state, row, col)
                count = neighbours['count']
                if (count == 2 or count == 3) and cls._cell(state, row, col) != '.':
                    next_cell_state = cls._cell(state, row, col)
                elif count == 3:
                    next_cell_state = neighbours['majority']
                else:
                    next_cell_state = '.'
                next_state += next_cell_state
        return next_state

    @classmethod
    def _get_neighbours(cls, state, r, c):
        neighbour_cells = []
        # :(
        if r > 0 and r < settings.ROWS and c > 0 and c < settings.COLUMNS:
            neighbour_cells.append(cls._cell(state, r - 1, c - 1))
            neighbour_cells.append(cls._cell(state, r - 1, c + 0))
            neighbour_cells.append(cls._cell(state, r - 1, c + 1))
            neighbour_cells.append(cls._cell(state, r + 0, c - 1))
            neighbour_cells.append(cls._cell(state, r + 0, c + 1))
            neighbour_cells.append(cls._cell(state, r + 1, c - 1))
            neighbour_cells.append(cls._cell(state, r + 1, c + 0))
            neighbour_cells.append(cls._cell(state, r + 1, c + 1))
        elif r == 0 and c > 0 and c < settings.COLUMNS:
            neighbour_cells.append(cls._cell(state, r + 0, c - 1))
            neighbour_cells.append(cls._cell(state, r + 0, c + 1))
            neighbour_cells.append(cls._cell(state, r + 1, c - 1))
            neighbour_cells.append(cls._cell(state, r + 1, c + 0))
            neighbour_cells.append(cls._cell(state, r + 1, c + 1))
        elif r == settings.ROWS and c > 0 and c < settings.COLUMNS:
            neighbour_cells.append(cls._cell(state, r - 1, c - 1))
            neighbour_cells.append(cls._cell(state, r - 1, c + 0))
            neighbour_cells.append(cls._cell(state, r - 1, c + 1))
            neighbour_cells.append(cls._cell(state, r + 0, c - 1))
            neighbour_cells.append(cls._cell(state, r + 0, c + 1))
        elif r > 0 and r < settings.ROWS and c == 0:
            neighbour_cells.append(cls._cell(state, r - 1, c + 0))
            neighbour_cells.append(cls._cell(state, r - 1, c + 1))
            neighbour_cells.append(cls._cell(state, r + 0, c + 1))
            neighbour_cells.append(cls._cell(state, r + 1, c + 0))
            neighbour_cells.append(cls._cell(state, r + 1, c + 1))
        elif r > 0 and r < settings.ROWS and c == settings.COLUMNS:
            neighbour_cells.append(cls._cell(state, r - 1, c - 1))
            neighbour_cells.append(cls._cell(state, r - 1, c + 0))
            neighbour_cells.append(cls._cell(state, r + 0, c - 1))
            neighbour_cells.append(cls._cell(state, r + 1, c - 1))
            neighbour_cells.append(cls._cell(state, r + 1, c + 0))
        elif r == 0 and c == 0:
            neighbour_cells.append(cls._cell(state, r + 0, c + 1))
            neighbour_cells.append(cls._cell(state, r + 1, c + 0))
            neighbour_cells.append(cls._cell(state, r + 1, c + 1))
        elif r == 0 and c == settings.COLUMNS:
            neighbour_cells.append(cls._cell(state, r + 0, c - 1))
            neighbour_cells.append(cls._cell(state, r + 1, c - 1))
            neighbour_cells.append(cls._cell(state, r + 1, c + 0))
        elif r == settings.ROWS and c == 0:
            neighbour_cells.append(cls._cell(state, r - 1, c + 0))
            neighbour_cells.append(cls._cell(state, r - 1, c + 1))
            neighbour_cells.append(cls._cell(state, r + 0, c + 1))
        elif r == settings.ROWS and c == settings.COLUMNS:
            neighbour_cells.append(cls._cell(state, r - 1, c - 1))
            neighbour_cells.append(cls._cell(state, r - 1, c + 0))
            neighbour_cells.append(cls._cell(state, r + 0, c - 1))

        neighbours = {}
        neighbours['count'] = len(neighbour_cells) - neighbour_cells.count('.')
        if neighbour_cells.count('1') > neighbour_cells.count('0'):
            neighbours['majority'] = '1'
        else:
            neighbours['majority'] = '0'
        return neighbours

    @staticmethod
    def _cell(state, r, c):
        return state[settings.ROWS * r + c]
