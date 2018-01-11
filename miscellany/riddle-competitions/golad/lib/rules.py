import settings
import next_cell_states


class Rules:
    @classmethod
    def calculate_next_state(cls, state):
        next_state = ''
        for row in range(settings.ROWS):
            for col in range(settings.COLUMNS):
                current_cell_state = state[settings.ROWS * row + col]

                neighbours = cls._get_neighbours(state, row, col)
                count = neighbours['count']
                if (count == 2 or count == 3) and current_cell_state!= '.':
                    next_cell_state = current_cell_state
                elif count == 3:
                    next_cell_state = neighbours['majority']
                else:
                    next_cell_state = '.'
                next_state += next_cell_state
        return next_state

    @classmethod
    def _get_neighbours(cls, state, r, c):
        neighbours = ''
        if r > 0 and r < settings.ROWS and c > 0 and c < settings.COLUMNS:
            # full cell
            neighbours += state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 2]
            neighbours += state[settings.ROWS * r + c - 1]
            neighbours += state[settings.ROWS * r + c + 1]
            neighbours += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 2]
            return next_cell_states.full_cell[neighbours]
        elif r == 0 and c > 0 and c < settings.COLUMNS:
            # top edge
            neighbours += state[settings.ROWS * r + c - 1]
            neighbours += state[settings.ROWS * r + c + 1]
            neighbours += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 2]
            return next_cell_states.edge_cell[neighbours]
        elif r == settings.ROWS and c > 0 and c < settings.COLUMNS:
            # bottom edge
            neighbours += state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 2]
            neighbours += state[settings.ROWS * r + c - 1]
            neighbours += state[settings.ROWS * r + c + 1]
            return next_cell_states.edge_cell[neighbours]
        elif r > 0 and r < settings.ROWS and c == 0:
            # left edge
            neighbours += state[settings.ROWS * (r - 1) + c:settings.ROWS * (r - 1) + c + 2]
            neighbours += state[settings.ROWS * r + c + 1]
            neighbours += state[settings.ROWS * (r + 1) + c:settings.ROWS * (r + 1) + c + 2]
            return next_cell_states.edge_cell[neighbours]
        elif r > 0 and r < settings.ROWS and c == settings.COLUMNS:
            # right edge
            neighbours += state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 1]
            neighbours += state[settings.ROWS * r + c - 1]
            neighbours += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 1]
            return next_cell_states.edge_cell[neighbours]
        elif r == 0 and c == 0:
            # top left corner
            neighbours += state[settings.ROWS * r + c + 1]
            neighbours += state[settings.ROWS * (r + 1) + c:settings.ROWS * (r + 1) + c + 2]
            return next_cell_states.corner_cell[neighbours]
        elif r == 0 and c == settings.COLUMNS:
            # top right corner
            neighbours += state[settings.ROWS * r + c - 1]
            neighbours += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 1]
            return next_cell_states.corner_cell[neighbours]
        elif r == settings.ROWS and c == 0:
            # bottom left corner
            neighbours += state[settings.ROWS * (r - 1) + c:settings.ROWS * (r - 1) + c + 2]
            neighbours += state[settings.ROWS * r + c + 1]
            return next_cell_states.corner_cell[neighbours]
        elif r == settings.ROWS and c == settings.COLUMNS:
            # bottom right corner
            neighbours += state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 1]
            neighbours += state[settings.ROWS * r + c - 1]
            return next_cell_states.corner_cell[neighbours]
