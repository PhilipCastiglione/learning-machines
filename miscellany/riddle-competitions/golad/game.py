from sys import stdin, stderr
import traceback

from settings import Settings
from bot import Bot


class Game:
    TICK_DURATION = 100  # we allow 100ms to pass between checks for input

    def __init__(self, settings):
        self.settings = settings
        self.round = 0
        self.bot = Bot(settings['your_botid'])

    def _handle_update(self, line):
        _, target, key, value = line.split()

        if target == 'game':
            stderr.write('[GAME] game update: {}\n'.format(line))  # TODO: remove
            if key == 'round':
                self.round = int(value)
            elif key == 'field':
                self.bot.update_current_node(value)
            else:
                raise Exception('Unrecognised game update', line)
        elif target in self.settings['player_names']:
            stderr.write('[GAME] player update: {}\n'.format(line))  # TODO: remove
            # no handling required
            pass
        else:
            raise Exception('Unrecognised update', line)

    @classmethod
    def start(cls):
        settings = Settings._parse_settings()
        game = cls(settings)
        cls._run_engine(game)

    @classmethod
    def _run_engine(cls, game):
        while True:
            try:
                line = stdin.readline().lower().strip()
                stderr.write('[GAME] line: {}\n'.format(line))  # TODO: remove

                # if we are waiting and don't have a line, the other player is
                # taking their turn, so keep building our search tree
                if len(line) <= 0:
                    game.bot.build_tree_for(cls.TICK_DURATION, game.settings['max_rounds'] - game.round)
                elif line.startswith('update'):
                    game._handle_update(line)
                elif line.startswith('action'):
                    # TODO: make time based decisions about building tree vs acting
                    t = game.settings['time_per_move'] - cls.TICK_DURATION
                    game.bot.build_tree_for(t, game.settings['max_rounds'] - game.round)
                    game.bot.move()
                elif line.startswith('quit'):
                    break
                else:
                    raise Exception('Unrecognised api message', line)

            # TODO: this?
            # except EOFError:
                # raise Exception('Exited due to EOFError')
            except KeyboardInterrupt:
                raise Exception('Exited via keyboard interrupt')
            except:
                # log the error but keep running if possible
                traceback.print_exc(file=stderr)
                stderr.flush()
