from .plant import Plant
from app.utilities import OrganismType, Directions, FieldState
import pygame
import copy
from random import randint

class Hogweed(Plant):
    ANIMALS_TO_KILL = [OrganismType.WOLF, OrganismType.TURTLE, OrganismType.ANTELOPE,
                       OrganismType.FOX, OrganismType.SHEEP, OrganismType.HUMAN]
    HOGWEED_GROWTH = 5      # chance in percents to regrow

    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 0, 99, "barszcz sosnowskiego", OrganismType.HOGWEED)
        image_path = Plant.ASSETS_PATH.joinpath("hogweed.png")
        self._image = pygame.image.load(image_path)

    @property
    def image(self):
        return self._image

    def collision(self, other_organism):
        if other_organism.org_type != OrganismType.CYBER_SHEEP:
            self._world.add_world_event(f'{other_organism.name} zjadl {self.name} i umarl')
            self._world.kill_organism(other_organism)
        else:
            tmp = self.position
            self._world.move_organism(other_organism, tmp)
        self._world.kill_organism(self)

    def action(self):
        self._kill_near_animals()

        if not self._world.draw_truth(5):
            return

        next_pos = self.get_next_available_position(self, Directions(randint(0, 3)))
        if next_pos.state == FieldState.AVAILABLE:
            self._world.add_organism(self._type, next_pos)

    def _kill_near_animals(self):
        for o in range(4):
            current = Directions(o)
            tmp = copy.deepcopy(self.position)
            if current == Directions.LEFT:
                tmp.x -= 1
            elif current == Directions.RIGHT:
                tmp.x += 1
            elif current == Directions.TOP:
                tmp.y -= 1
            elif current == Directions.BOTTOM:
                tmp.y += 1

            if self._world.get_field_state(tmp) == FieldState.OCCUPIED:
                organism = self._world.get_organism_by_pos(tmp)
                org_type = organism.org_type
                if org_type in Hogweed.ANIMALS_TO_KILL:
                    self._world.add_world_event(f'{self.name} zabil sasiada {organism.name}')
                    self._world.kill_organism(organism)