from sys import stdout
import time
from operator import attrgetter

from tree import Tree


class Bot:
    def __init__(self):
        self.tree = Tree()

    def build_tree_for(self, duration):
        now = time.perf_counter()

        # TODO: improve this naive implementation
        if not self.tree.current_node.children:
            self.tree.current_node.build_children()

        # OH NO YOU HAVE NO CPU
        #if 1000 * (time.perf_counter() - now) >= duration:
            #return

        #for c in self.tree.current_node.children:
            #if not c.children:
                #c.build_children()

        #if 1000 * (time.perf_counter() - now) >= duration:
            #return

        #for c in self.tree.current_node.children:
            #for c2 in c.children:
                #if not c2.children:
                    #c2.build_children()

    def move(self):
        # pick the best move from the available children
        node = max(self.tree.current_node.children, key=attrgetter('minimax_value'))
        stdout.write('{}\n'.format(node.move))
        stdout.flush()
