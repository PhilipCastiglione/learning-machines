from node import Node
import settings


class Tree:
    def __init__(self):
        self.current_node = None

    def set_current_node(self, state):
        if self.current_node == None:
            # The starting state of the game. The first move is always by '0'.
            my_turn = settings.PLAYER_ID == '0'
            self.current_node = Node(state, my_turn, None, None)
        else:
            # Find the next node, using the node state, in the current node's children.
            next_node = next((n for n in self.current_node.children if n.state == state), None)

            if next_node == None:
                # The opponent made a move we haven't explored (hopefully it was bad)
                self.current_node = Node(state, False, None, None)
            else:
                # Remove references to the parent so it and the next nodes siblings
                # can be garbage collected.
                next_node.parent = None
                self.current_node = next_node
