import settings


class Field:
    def __init__(self, state):
        self.state = state
        self.heuristic_value = self._calculate_heuristic()

    def _calculate_heuristic(self):
        cell_count = self.state.count(settings.PLAYER_ID)
        opponent_cell_count = self.state.count(settings.OPPONENT_ID)

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
