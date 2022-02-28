from .plant import Plant
from worldsimulator.utilities import OrganismType
import pygame


class Guarana(Plant):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 0, 0, "guarana", OrganismType.GUARANA)
        image_path = Plant.ASSETS_PATH.joinpath("guarana.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def collision(self, other_organism):
        self._world.add_world_event(f'{other_organism.name} ate {self.name} '
                                    f'and has {other_organism.strength + 3} strength')
        tmp = self.position
        self._world.move_organism(other_organism, tmp)
        other_organism.strength += 3
        self._world.kill_organism(self)
