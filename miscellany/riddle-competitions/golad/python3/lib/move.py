import settings
from move_type import MoveType


class Move:
    def __init__(self, move_type, target, sacrifice):
        self.move_type = move_type
        self.target = target
        self.sacrifice = sacrifice

    def __str__(self):
        if self.move_type == MoveType.BIRTH:
            target_string = "{},{}".format(self.target % settings.COLUMNS, self.target // settings.COLUMNS)
            sacrifice_string = "{},{}".format(self.sacrifice[0] % settings.COLUMNS, self.sacrifice[0] // settings.COLUMNS)
            sacrifice_string += " {},{}".format(self.sacrifice[1] % settings.COLUMNS, self.sacrifice[1] // settings.COLUMNS)
            return '{} {} {}'.format(self.move_type, target_string, sacrifice_string)
        elif self.move_type == MoveType.KILL:
            target_string = "{},{}".format(self.target % settings.COLUMNS, self.target // settings.COLUMNS)
            return '{} {}'.format(self.move_type, target_string)
        elif self.move_type == MoveType.PASS:
            return str(self.move_type)
        else:
            raise Exception('Unrecognised move type on node')
