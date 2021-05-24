from .animal import Animal
from ...utilities import OrganismType
import pygame


class Wolf(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 5, 9, "Wolf", OrganismType.WOLF)
        image_path = Animal.ASSETS_PATH.joinpath("wolf.bmp")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image
