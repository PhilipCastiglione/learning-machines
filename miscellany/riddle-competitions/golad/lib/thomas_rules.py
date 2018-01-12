import settings
import next_cell_states


class ThomasRules:
    @classmethod
    def calculate_next_state(cls, state):
        next_state = [''] * 288
        i = 0
        for row in range(settings.ROWS):
            for col in range(settings.COLUMNS):
                next_state[i] = cls._get_next_cell_state(state, row, col)
                i += 1
        return ''.join(next_state)

    @staticmethod
    def _get_next_cell_state(state, r, c):
        if r > 0 and r < settings.ROWS and c > 0 and c < settings.COLUMNS:
            # full cell
            cell_region = state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 2]
            cell_region += state[settings.ROWS * r + c - 1:settings.ROWS * r + c + 2]
            cell_region += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 2]
            return '.'
        elif r == 0 and c > 0 and c < settings.COLUMNS:
            # top edge
            cell_region = state[settings.ROWS * r + c - 1:settings.ROWS * r + c + 2]
            cell_region += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 2]
            return '.'
        elif r == settings.ROWS and c > 0 and c < settings.COLUMNS:
            # bottom edge
            cell_region = state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 2]
            cell_region += state[settings.ROWS * r + c - 1:settings.ROWS * r + c + 2]
            return '.'
        elif r > 0 and r < settings.ROWS and c == 0:
            # left edge
            cell_region = state[settings.ROWS * (r - 1) + c:settings.ROWS * (r - 1) + c + 2]
            cell_region += state[settings.ROWS * r + c:settings.ROWS * r + c + 2]
            cell_region += state[settings.ROWS * (r + 1) + c:settings.ROWS * (r + 1) + c + 2]
            return '.'
        elif r > 0 and r < settings.ROWS and c == settings.COLUMNS:
            # right edge
            cell_region = state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 1]
            cell_region += state[settings.ROWS * r + c - 1:settings.ROWS * r + c + 1]
            cell_region += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 1]
            return '.'
        elif r == 0 and c == 0:
            # top left corner
            cell_region = state[settings.ROWS * r + c:settings.ROWS * r + c + 2]
            cell_region += state[settings.ROWS * (r + 1) + c:settings.ROWS * (r + 1) + c + 2]
            return '.'
        elif r == 0 and c == settings.COLUMNS:
            # top right corner
            cell_region = state[settings.ROWS * r + c - 1:settings.ROWS * r + c + 1]
            cell_region += state[settings.ROWS * (r + 1) + c - 1:settings.ROWS * (r + 1) + c + 1]
            return '.'
        elif r == settings.ROWS and c == 0:
            # bottom left corner
            cell_region = state[settings.ROWS * (r - 1) + c:settings.ROWS * (r - 1) + c + 2]
            cell_region += state[settings.ROWS * r + c:settings.ROWS * r + c + 2]
            return '.'
        elif r == settings.ROWS and c == settings.COLUMNS:
            # bottom right corner
            cell_region = state[settings.ROWS * (r - 1) + c - 1:settings.ROWS * (r - 1) + c + 1]
            cell_region += state[settings.ROWS * r + c - 1:settings.ROWS * r + c + 1]
            return '.'

    def calculate_heuristic(state, my_turn):
        if my_turn:
            player_id = settings.PLAYER_ID
            opponent_id = settings.OPPONENT_ID
        else:
            opponent_id = settings.PLAYER_ID
            player_id = settings.OPPONENT_ID

        cell_count = state.count(player_id)
        opponent_cell_count = state.count(opponent_id)

        if opponent_cell_count == 0:
            # if the opponent has no cells left, this is a win, set to max
            value = settings.ROWS * settings.COLUMNS
        elif cell_count == 0:
            # if you have no cells left, this is a loss, set to min
            value = 0
        else:
            # otherwise use the difference between your and their live cells
            value = cell_count - opponent_cell_count

        return value
