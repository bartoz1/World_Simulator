from .plant import Plant
from app.utilities import OrganismType
import pygame


class WolfBerries(Plant):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 0, 99, "wilcze jagody", OrganismType.WOLF_BERRIES)
        image_path = Plant.ASSETS_PATH.joinpath("wolf_berries.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def collision(self, other_organism):
        self._world.add_world_event(f'{other_organism.name} zjadl {self.name} i umarl')
        self._world.kill_organism(other_organism)
        self._world.kill_organism(self)
