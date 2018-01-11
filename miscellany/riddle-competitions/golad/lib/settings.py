from sys import stdin
import time

# globals to be set when settings are parsed
TICK_DURATION = None
PLAYER_NAMES = None
TIME_PER_MOVE = None
PLAYER_ID = None
OPPONENT_ID = None
ROWS = None
COLUMNS = None

class Settings:
    """
    Seperate parsing settings from game instance logic. All the settings come
    at the start of the game, in a set of lines via stdin. We parse them then
    load the ones we need into the global scope.
    """
    STRING_SETTINGS = [
        'your_bot',
        'your_botid'
    ]
    NUMERICAL_SETTINGS = [
        'timebank',
        'time_per_move',
        'field_width',
        'field_height',
        'max_rounds'
    ]
    CSV_SETTINGS = [
        'player_names'
    ]

    @classmethod
    def parse_settings(cls):
        settings = {}
        while True:
            line = stdin.readline().lower().strip()

            # wait until we have a line
            if len(line) <= 0:
                time.sleep(0.01)
                continue

            if not line.startswith('settings'):
                # The first message after the settings should be update game
                # round 0, which we can safely throw away.
                if not line == 'update game round 0':
                    raise Exception('Threw away important line')
                break
            else:
                cls._add_setting(settings, line)

        cls._load_settings(settings)

    @classmethod
    def _add_setting(cls, settings, line):
        _, key, value = line.split()

        if key in cls.STRING_SETTINGS:
            settings[key] = value
        elif key in cls.NUMERICAL_SETTINGS:
            settings[key] = int(value)
        elif key in cls.CSV_SETTINGS:
            settings[key] = value.split(',')
        else:
            raise Exception('Unrecognised setting', line)

    @staticmethod
    def _load_settings(settings):
        g = globals()
        g['TICK_DURATION'] = 100  # we allow 100ms to pass between checks for input
        g['PLAYER_NAMES'] = settings['player_names']
        g['TIME_PER_MOVE'] = settings['time_per_move']
        g['PLAYER_ID'] = settings['your_botid']
        g['OPPONENT_ID'] = str(1 - int(settings['your_botid']))
        g['ROWS'] = settings['field_height']
        g['COLUMNS'] = settings['field_width']