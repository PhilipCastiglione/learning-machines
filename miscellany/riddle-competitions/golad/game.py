from sys import stdin, stderr
import traceback

import settings
from bot import Bot


class Game:
    def __init__(self):
        self.round = 0
        self.bot = Bot()

    def _handle_update(self, line):
        _, target, key, value = line.split()

        if target == 'game':
            if key == 'round':
                self.round = int(value)
            elif key == 'field':
                self.bot.tree.set_current_node(value.replace(',', ''))
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

                # if we are waiting and don't have a line, the other player is
                # taking their turn, so keep building our search tree
                if len(line) <= 0:
                    game.bot.build_tree_for(settings.TICK_DURATION)
                elif line.startswith('update'):
                    game._handle_update(line)
                elif line.startswith('action'):
                    # TODO: make time based decisions about building tree vs acting
                    t = settings.TIME_PER_MOVE - settings.TICK_DURATION
                    game.bot.build_tree_for(t)
                    game.bot.move()
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
