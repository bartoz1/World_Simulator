from enum import Enum
from dataclasses import dataclass


class Options(Enum):
    NEW_GAME = 0
    LOAD_GAME = 1
    OPTIONS = 2
    EXIT = 3


class OrganismType(Enum):
    HUMAN = 0
    WOLF = 1
    SHEEP = 2
    FOX = 3
    TURTLE = 4
    ANTELOPE = 5
    GRASS = 6
    DANDELION = 7
    GUARANA = 8
    WOLF_BERRIES = 9
    HOGWEED = 10
    CYBER_SHEEP = 11


class Directions(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def next(self):
        if self.value == 3:
            return Directions(0)
        return Directions(self.value + 1)


class FieldState(Enum):
    AVAILABLE = 0
    OCCUPIED = 1
    BORDER = 2
    NOTAVAILABLE = 3
    UNKNOWN = 4


@dataclass
class Position:
    x: int
    y: int
    state: FieldState = FieldState.UNKNOWN

    def __str__(self):
        return f'({self.x}, {self.y})'

