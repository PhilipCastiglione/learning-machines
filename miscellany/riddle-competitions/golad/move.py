from move_type import MoveType


class Move:
    def __init__(self, field):
        self.move_type = field.move_type
        self.target = field.target
        self.sacrifice = field.sacrifice

    def __str__(self):
        if self.move_type == MoveType.BIRTH:
            sacrifice_string = ' '.join(str(p) for p in self.sacrifice)
            return '{} {} {}'.format(self.move_type, self.target, sacrifice_string)
        elif self.move_type == MoveType.KILL:
            return '{} {}'.format(self.move_type, self.target)
        elif self.move_type == MoveType.PASS:
            return str(self.move_type)
        else:
            raise Exception('Unrecognised move type on node')
