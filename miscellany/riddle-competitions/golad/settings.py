from sys import stdin
import time


class Settings:
    """
    Seperate parsing settings from game instance logic. All the settings come
    at the start of the game, in a set of lines via stdin.
    """
    # TODO: explain how each is used (or not)
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
    def _parse_settings(cls):
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

        return settings

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
