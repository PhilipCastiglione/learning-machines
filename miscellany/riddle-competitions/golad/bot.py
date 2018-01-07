from sys import stdin, stderr
import time

class Bot:
    def build_tree_for(self, duration):
        stderr.write('[BOT] building tree for {}\n'.format(duration))  # TODO: remove
        time.sleep(duration / 1000.0)

    def set_current_node(self, field):
        stderr.write('[BOT] setting current node\n')  # TODO: remove

    def move(self):
        stderr.write('[BOT] making move\n')  # TODO: remove
