from enum import Enum


class MoveType(Enum):
    KILL = 'kill'
    BIRTH = 'birth'
    PASS = 'pass'

    def __str__(self):
        return self.value
