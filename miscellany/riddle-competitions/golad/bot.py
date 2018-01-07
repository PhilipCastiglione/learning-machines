from sys import stderr, stdout
import time
from operator import attrgetter

from field import Field
from move import Move


class Bot:
    def __init__(self, player_id):
        self.player_id = player_id
        self.current_node = None

    def build_tree_for(self, duration, depth_limit):
        stderr.write('[BOT] building tree for {}\n'.format(duration))  # TODO: remove

        # TODO: is this needed?
        if self.current_node == None:
            stderr.write('[BOT] building tree but current node is none\n')  # TODO: remove
            return

        now = time.perf_counter()

        # TODO: fix this naive implementation
        if not self.current_node.children:
            self.current_node.build_children()

        if 1000 * (time.perf_counter() - now) >= duration:
            stderr.write('[BOT] built current node children now returning\n')  # TODO: remove
            return

        for c in self.current_node.children:
            if not c.children:
                c.build_children()

        if 1000 * (time.perf_counter() - now) >= duration:
            stderr.write('[BOT] built depth 2 children now returning\n')  # TODO: remove
            return

        for c in self.current_node.children:
            for c2 in c.children:
                if not c2.children:
                    c2.build_children()

        if 1000 * (time.perf_counter() - now) >= duration:
            stderr.write('[BOT] built depth 2 children now returning\n')  # TODO: remove
            return

        stderr.write('[BOT] could have started depth 3 children\n')  # TODO: remove

    def update_current_node(self, field_data):
        stderr.write('[BOT] setting current node\n')  # TODO: remove
        if self.current_node == None:
            # for the first move of the game
            first_player = '0'
            self.current_node = Field(field_data, first_player, self.player_id == first_player)
        else:
            next_node = next((n for n in self.current_node.children if n.data == field_data), None)

            if next_node == None:
                raise Exception('Updating current node but node not found in children')
            else:
                next_node.parent = None
                self.current_node = next_node

    def move(self):
        stderr.write('[BOT] making move\n')  # TODO: remove
        node = max(self.current_node.children, key=attrgetter('minimax_value'))
        move = Move(node)
        stdout.write('{}\n'.format(move))
        stdout.flush()
