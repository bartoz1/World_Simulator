from .animal import Animal
from app.utilities import OrganismType
import pygame


class Sheep(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 4, 4, "owca", OrganismType.SHEEP)
        image_path = Animal.ASSETS_PATH.joinpath("sheep.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image