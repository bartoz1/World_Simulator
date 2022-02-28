from .plant import Plant
from app.utilities import OrganismType, Directions, FieldState
import pygame


class Dandelion(Plant):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 0, 0, "dandelion", OrganismType.DANDELION)
        image_path = Plant.ASSETS_PATH.joinpath("dandelion.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def action(self):
        """ tries to regrown 3 times"""
        for o in range(3):
            if self._world.draw_truth(Plant.PLANT_GROWTH):
                next_pos = self.get_next_available_position(self, Directions.LEFT)
                if next_pos.state == FieldState.AVAILABLE:
                    self._world.add_organism(self._type, next_pos)