from sys import stdin, stderr, stdout
from operator import attrgetter
import traceback
import time

import settings
from node import Node


class Game:
    def __init__(self):
        self.round = 0
        self.current_node = None

    def _handle_update(self, line):
        _, target, key, value = line.split()

        if target == 'game':
            if key == 'round':
                self.round = int(value)
            elif key == 'field':
                state = value.replace(',','')
                self.current_node = Node(state, True, None, None)
            else:
                raise Exception('Unrecognised game update', line)
        elif target in settings.PLAYER_NAMES:
            # no action required
            pass
        else:
            raise Exception('Unrecognised update', line)

    @classmethod
    def start(cls):
        settings.Settings.parse_settings()
        game = cls()
        cls._run_engine(game)

    @staticmethod
    def _run_engine(game):
        while True:
            try:
                line = stdin.readline().lower().strip()

                if len(line) <= 0:
                    time.sleep(0.01)
                elif line.startswith('update'):
                    game._handle_update(line)
                elif line.startswith('action'):
                    game.current_node.build_children()
                    game.move()
                elif line.startswith('quit'):
                    break
                else:
                    raise Exception('Unrecognised api message', line)

            except KeyboardInterrupt:
                raise Exception('Exited via keyboard interrupt')
            except:
                # log the error but keep running if possible
                traceback.print_exc(file=stderr)
                stderr.flush()

    def move(self):
        # pick the best move from the available children
        node = max(self.current_node.children, key=attrgetter('minimax_value'))
        stdout.write('{}\n'.format(node.move))
        stdout.flush()
