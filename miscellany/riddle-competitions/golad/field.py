from operator import attrgetter


class Field:
    def __init__(self, data, player_id, turn_player_id, parent=None, move_type=None, target=None, sacrifice=None):
        self.data = data
        self.player_id = player_id
        self.turn_player_id = turn_player_id
        self.opponent_id = str(1 - int(turn_player_id))
        self.parent = parent
        self.move_type = move_type
        self.target = target
        self.sacrifice = sacrifice
        self.heuristic_value = self._heuristic_value()
        self.minimax_value = self.heuristic_value
        self.children = []

    def build_children(self):
        # TODO: implement
        # build pass
        # build kill children
        # build birth children
        self._update_minimax()

    def _update_minimax(self):
        # If this turn is ours, then the next turn is our opponents, assume they
        # choose their best option and select the minimum value for us. If it's
        # their turn, we will choose our best option next.
        if self.player_id == self.turn_player_id:
            self.minimax_value = min(self.children, key=attrgetter('minimax_value'))
        else:
            self.minimax_value = max(self.children, key=attrgetter('minimax_value'))

        # trigger recalculation up the tree
        if self.parent:
            self.parent._update_minimax()

    def _heuristic_value(self):
        cell_count = self.data.count(self.turn_player_id)
        opponent_cell_count = self.data.count(self.opponent_id)

        if opponent_cell_count == 0:
            # if the opponent has no cells left, this is a win, set to max
            value = 288
        elif cell_count == 0:
            # if the opponent has no cells left, this is a win, set to min
            value = 0
        else:
            # otherwise use the difference between your and their live cells
            value = cell_count - opponent_cell_count

        return value
