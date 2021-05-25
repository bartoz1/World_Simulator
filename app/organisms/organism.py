from abc import ABC, abstractmethod
from ..utilities import OrganismType, Position, Directions, FieldState
import copy

class Organism(ABC):

    def __init__(self, world, pos_x, pos_y, initiative: int, strength: int, name: str, organism_type: OrganismType):
        self._world = world
        self._is_alive = True
        self._strength = strength
        self._initiative = initiative
        self._age = 1
        self._position = Position(pos_x, pos_y, FieldState.OCCUPIED)
        self._name = name
        self._type = organism_type

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other_organism):
        pass

    @property
    @abstractmethod
    def image(self):
        pass

    def will_survive_attack(self, other_organism: 'Organism') -> bool:
        """ Compares given organism to self (strength and age) and decides if it will survive the attack"""
        if other_organism.strength >= self.strength:
            return False
        return True

    def get_next_available_position(self, organism: 'Organism', desired_dir: Directions):
        """ Checks every field surrounding current position and returns first available starting from desired_dir """
        for i in range(4):
            tmp = copy.deepcopy(organism.position)
            if desired_dir == Directions.LEFT:
                tmp.x -= 1
            elif desired_dir == Directions.RIGHT:
                tmp.x += 1
            elif desired_dir == Directions.TOP:
                tmp.y -= 1
            elif desired_dir == Directions.BOTTOM:
                tmp.y += 1

            if organism._world.get_field_state(tmp) == FieldState.AVAILABLE:
                return tmp
            desired_dir = desired_dir.next()
        return copy.deepcopy(organism._position)

    # SETTERS AND GETTERS
    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, new_str):
        self._strength = new_str

    @property
    def initiative(self):
        return self._initiative

    @initiative.setter
    def initiative(self, new_ini):
        self._initiative = new_ini

    @property
    def is_alive(self):
        return self._is_alive

    @is_alive.setter
    def is_alive(self, new_alive):
        self._is_alive = new_alive

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new):
        self._age = new

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new: Position):
        self._position = new

    @property
    def name(self):
        return self._name

    def increment_age(self):
        self._age += 1

    def set_death(self):
        self._is_alive = False

    def __lt__(self, other: 'Organism'):
        if self.initiative == other.initiative:
            return self.age > other.age
        return self.initiative > other.initiative

    def __gt__(self, other: 'Organism'):
        if self.initiative == other.initiative:
            return self.age < other.age
        return self.initiative < other.initiative
