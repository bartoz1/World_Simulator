from .animal import Animal
from ...utilities import OrganismType, Directions, FieldState
import pygame
import copy


class Fox(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 7, 3, "Lis", OrganismType.FOX)
        image_path = Animal.ASSETS_PATH.joinpath("fox.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def get_next_position(self, desired_dir: Directions):
        """ Checks every field surrounding current position and returns
            first not border and if possible not occupied pos starting from desired_dir """
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
                if f_state == FieldState.OCCUPIED and self._world.get_organism_by_pos(tmp).initiative <= self.initiative:
                    return tmp
                elif self._world.get_field_state(tmp) == FieldState.AVAILABLE:
                    return tmp

            desired_dir = desired_dir.next()
        return copy.deepcopy(self._position)
