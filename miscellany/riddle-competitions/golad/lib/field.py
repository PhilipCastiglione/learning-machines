import settings


class Field:
    def __init__(self, state, my_turn):
        self.state = state
        self.heuristic_value = self._calculate_heuristic(my_turn)

    def _calculate_heuristic(self, my_turn):
        if my_turn:
            player_id = settings.PLAYER_ID
            opponent_id = settings.OPPONENT_ID
        else:
            opponent_id = settings.PLAYER_ID
            player_id = settings.OPPONENT_ID

        cell_count = self.state.count(player_id)
        opponent_cell_count = self.state.count(opponent_id)

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
