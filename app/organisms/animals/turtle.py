from .animal import Animal
from ...utilities import OrganismType, Directions, FieldState
import pygame
import copy
from ..organism import Organism


class Turtle(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 1, 2, "zolw", OrganismType.TURTLE)
        image_path = Animal.ASSETS_PATH.joinpath("turtle.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def get_next_position(self, desired_dir: Directions):
        """  75% chance not to move but if moves - checks every field surrounding current position and returns
            first not border and if possible not occupied pos starting from desired_dir """
        if self._world.draw_truth(75):
            tmp = copy.deepcopy(self._position)
            tmp.state = FieldState.UNKNOWN
            return tmp

        for i in range(4):
            tmp = copy.deepcopy(self.position)
            if desired_dir == Directions.LEFT:
                tmp.x -= 1
            elif desired_dir == Directions.RIGHT:
                tmp.x += 1
            elif desired_dir == Directions.TOP:
                tmp.y -= 1
            elif desired_dir == Directions.BOTTOM:
                tmp.y += 1

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
                    f'rozmnazanie {self.name} z {other_organism.name} niemozliwe ze wzgledu na wiek')
        elif other_organism.strength < 5:
            self._world.add_world_event(
                f'{self.name} odparl atak {other_organism.name} ')
        else:
            self._world.add_world_event(f'{other_organism.name} zabilo {self.name} {self.position}')
            tmp = self.position
            self._world.move_organism(other_organism, tmp)
            self._world.kill_organism(self)
