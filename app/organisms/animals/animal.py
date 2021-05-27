from abc import ABC, abstractmethod
from ..organism import Organism
from ...utilities import OrganismType, Directions, FieldState
from random import randint
import copy
from pathlib import Path


class Animal(Organism, ABC):
    REPROD_AGE = 4  # age that allows animals to reproduce
    ASSETS_PATH = Path(__file__).parents[2].joinpath("assets")

    def __init__(self, world, pos_x, pos_y, initiative: int, strength: int, name: str, organism_type: OrganismType):
        super().__init__(world, pos_x, pos_y, initiative, strength, name, organism_type)

    def action(self):
        """ Moves the animal to random position """
        print(f'{self.name} ini: {self.initiative}')
        move_dir = Directions(randint(0, 3))
        next_pos = self.get_next_position(move_dir)
        print(f'przemieszczenie: {move_dir} - {next_pos}')
        if next_pos.state == FieldState.NOTAVAILABLE:                           # no available moves
            self._world.add_world_event(f'{self.name} nie moze sie poruszyc')
        elif next_pos.state == FieldState.OCCUPIED:                             # collision with other organism
            other_organism = self._world.get_organism_by_pos(next_pos)
            other_organism.collision(self)
        elif next_pos.state == FieldState.AVAILABLE:                            # moves to available position
            self._world.add_world_event(f'{self.name} moved to: ({next_pos.x}, {next_pos.y})')
            self._world.move_organism(self, next_pos)
        else:
            self._world.add_world_event(f'{self.name} stoi')

    def collision(self, other_organism: Organism):
        """ collision handler - if attacker is the same type that performs reproduction, in other case fight """
        if self.name == other_organism.name:                                                # both organisms are same type
            if self.age > Animal.REPROD_AGE and other_organism.age > Animal.REPROD_AGE:     # checking organisms age
                self._give_birth(other_organism)
            else:
                self._world.add_world_event(f'rozmnazanie {self.name} z {other_organism.name} niemozliwe (wiek)')
        elif self.will_survive_attack(other_organism):
            # death of attacker
            self._world.add_world_event(f'{other_organism.name} zmarl atakujac {self.name} {self.position}')
            self._world.kill_organism(other_organism)
        else:       # attacker kills prey
            self._world.add_world_event(f'{other_organism.name} zabilo {self.name} {self.position}')
            tmp = self.position
            self._world.move_organism(other_organism, tmp)
            self._world.kill_organism(self)

    def get_next_position(self, desired_dir: Directions):
        """ Checks every field surrounding current position and returns first not border starting from desired_dir """

        for i in range(4):
            tmp = copy.deepcopy(self._position)
            if desired_dir == Directions.LEFT:
                tmp.x -= 1
            elif desired_dir == Directions.RIGHT:
                tmp.x += 1
            elif desired_dir == Directions.TOP:
                tmp.y -= 1
            elif desired_dir == Directions.BOTTOM:
                tmp.y += 1

            if self._world.get_field_state(tmp) != FieldState.BORDER:
                return tmp
            desired_dir = desired_dir.next()
        return copy.deepcopy(self._position)

    def _give_birth(self, parent2: Organism):
        self._world.add_world_event(f'maja potomstwo: {self.name} z {parent2.name}')

        next_pos = self.get_next_available_position(self, Directions(randint(0,3)))
        if not self._world.are_diferent_positions(next_pos, self.position):        # new position is = to parent1 position
            next_pos = self.get_next_available_position(parent2, Directions(randint(0,3)))

        if not self._world.are_diferent_positions(next_pos, parent2.position):     # still new position if = to parent2 position
            self._world.add_world_event(f'potomstwo umarlo')
        else:
            self._world.add_organism(self._type, next_pos)
