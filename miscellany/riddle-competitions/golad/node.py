from operator import attrgetter

from field import Field
from rules import Rules
from move_type import MoveType


class Node:
    def __init__(self, state, my_turn, parent, move_type):
        self.field = Field(state)
        self.my_turn = my_turn
        self.parent = parent
        self.move_type = move_type
        self.children = []
        self.minimax_value = self.field.heuristic_value

    def build_children(self):
        self._build_pass()
        self._build_kill()
        self._build_birth()
        self._update_minimax()

    def _build_pass(self):
        # passing doesn't change the intermediate state
        intermediate_state = self.field.state
        child_state = Rules.calculate_next_state(intermediate_state)
        print(child_state) # TODO: remove
        child = Node(child_state, not self.my_turn, self, MoveType.PASS)
        self.children.append(child)

    def _build_kill(self):
        # TODO: implement
        pass

    def _build_birth(self):
        # TODO: implement
        pass

    def _update_minimax(self):
        if self.my_turn:
            # If it's our turn, the node's children are our opponents turn. Assume
            # they choose their best move and select the minimum value for us.
            self.minimax_value = min(self.children, key=attrgetter('minimax_value'))
        else:
            # If it's their turn, we will choose our best move from the children.
            self.minimax_value = max(self.children, key=attrgetter('minimax_value'))

        # Trigger recalculation up the tree
        if self.parent:
            self.parent._update_minimax()
