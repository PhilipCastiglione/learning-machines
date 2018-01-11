from operator import attrgetter, itemgetter
import itertools

import settings
from field import Field
from rules import Rules
from move_type import MoveType


class Node:
    def __init__(self, state, my_turn, parent, move_type, target=None, sacrifice=None):
        self.field = Field(state, my_turn)
        self.my_turn = my_turn
        self.parent = parent
        self.move_type = move_type
        self.target = target
        self.sacrifice = sacrifice
        self.children = []
        self.minimax_value = self.field.heuristic_value
        self.best_kill_moves = []

    def build_children(self):
        self._build_pass()
        self._build_kill()
        self._filter_best_kill_moves()
        self._build_birth()
        self._update_minimax()

    def _build_pass(self):
        # passing doesn't change the intermediate state
        child_state = Rules.calculate_next_state(self.field.state)
        child = Node(child_state, not self.my_turn, self, MoveType.PASS)
        self.children.append(child)

    def _build_kill(self):
        for idx, cell in enumerate(self.field.state):
            if cell != '.':
                s = self.field.state
                s = s[:idx] + '.' + s[(idx + 1):]
                child_state = Rules.calculate_next_state(s)
                child = Node(child_state, not self.my_turn, self, MoveType.KILL, idx)
                if cell == settings.PLAYER_ID:
                    self.best_kill_moves.append({'idx': idx, 'score': child.minimax_value})
                self.children.append(child)

    def _filter_best_kill_moves(self):
        self.best_kill_moves.sort(key=itemgetter('score'))
        self.best_kill_moves = self.best_kill_moves[-settings.TOP_KILL_COUNT:]

    def _build_birth(self):
        for idx, cell in enumerate(self.field.state):
            if cell == '.':
                for a, b in itertools.combinations(self.best_kill_moves, 2):
                    a_idx = a['idx']
                    b_idx = b['idx']

                    s = self.field.state
                    s = s[:idx] + settings.PLAYER_ID + s[(idx + 1):]
                    s = s[:a_idx] + '.' + s[(a_idx + 1):]
                    s = s[:b_idx] + '.' + s[(b_idx + 1):]
                    child_state = Rules.calculate_next_state(s)
                    child = Node(child_state, not self.my_turn, self, MoveType.BIRTH, idx, (a_idx, b_idx))
                    self.children.append(child)

    def _update_minimax(self):
        if self.my_turn:
            # If it's our turn, the node's children are our opponents turn. Assume
            # they choose their best move and select the minimum value for us.
            self.minimax_value = min(self.children, key=attrgetter('minimax_value')).minimax_value
        else:
            # If it's their turn, we will choose our best move from the children.
            self.minimax_value = max(self.children, key=attrgetter('minimax_value')).minimax_value

        # Trigger recalculation up the tree
        if self.parent:
            self.parent._update_minimax()
