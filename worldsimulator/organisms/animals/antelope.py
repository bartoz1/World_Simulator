from .animal import Animal
from ...utilities import OrganismType, Directions, FieldState
import pygame
import copy
from ..organism import Organism


class Antelope(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 4, 4, "antelope", OrganismType.ANTELOPE)
        image_path = Animal.ASSETS_PATH.joinpath("antelope.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def get_next_position(self, desired_dir: Directions):
        """ Checks every field surrounding current position and returns
            first not border and if possible not occupied pos starting from desired_dir """
        for j in range(2, 0, -1):
            for i in range(4):
                tmp = copy.deepcopy(self.position)
                if desired_dir == Directions.LEFT:
                    tmp.x -= j
                elif desired_dir == Directions.RIGHT:
                    tmp.x += j
                elif desired_dir == Directions.TOP:
                    tmp.y -= j
                elif desired_dir == Directions.BOTTOM:
                    tmp.y += j

                f_state = self._world.get_field_state(tmp)
                if f_state != FieldState.BORDER:
                    return tmp
                desired_dir = desired_dir.next()
        tmp = copy.deepcopy(self._position)
        tmp.state = FieldState.NOTAVAILABLE
        return tmp

    def collision(self, other_organism: Organism):
        """ collision handler - if attacker is the same type that performs reproduction, in other case fight but with
            50% chance to escape """
        if self.name == other_organism.name:  # both organisms are same type
            if self.age > Animal.REPROD_AGE and other_organism.age > Animal.REPROD_AGE:  # checking organisms age
                self._give_birth(other_organism)
            else:
                self._world.add_world_event(
                    f'reproduction {self.name} with {other_organism.name} not possible (age)')
        else:
            if self._world.draw_truth(50):
                next_pos = self.get_next_available_position(self, Directions.LEFT)

                if self._world.are_diferent_positions(self.position, next_pos):
                    """ animal finds an available field to escape so escapes """
                    self._world.add_world_event(
                        f'{self.name} ran away from the {other_organism.name}')
                    tmp = copy.deepcopy(self._position)
                    self._world.move_organism(self, next_pos)
                    self._world.move_organism(other_organism, tmp)
                    return
            if self.will_survive_attack(other_organism):
                """ attacker dies trying to kill this organism """
                self._world.add_world_event(
                    f'{other_organism.name} died attacking {self.name} {self.position}')
                self._world.kill_organism(other_organism)

            else:
                """ attacker kills prey - this object """
                self._world.add_world_event(f'{other_organism.name} killed {self.name} {self.position}')
                tmp = self.position
                self._world.move_organism(other_organism, tmp)
                self._world.kill_organism(self)
