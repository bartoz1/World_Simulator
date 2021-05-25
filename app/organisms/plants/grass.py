from .plant import Plant
from app.utilities import OrganismType
import pygame


class Grass(Plant):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 0, 0, "trawa", OrganismType.GRASS)
        image_path = Plant.ASSETS_PATH.joinpath("grass.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image