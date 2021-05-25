from abc import ABC

from ..organism import Organism
from app.utilities import OrganismType, Directions, FieldState
from random import randint


class Plant(Organism, ABC):
    PLANT_GROWTH = 13   # chance in percents to regrow

    def __init__(self, world, pos_x, pos_y, initiative: int, strength: int, name: str, organism_type: OrganismType):
        super().__init__(world, pos_x, pos_y, initiative, strength, name, organism_type)

    def action(self):
        if not self._world.draw_truth(Plant.PLANT_GROWTH):
            return
        next_pos = self.get_next_available_position(self, Directions(randint(0, 3)))
        if next_pos.state == FieldState.AVAILABLE:
            self._world.add_organism(self._type, next_pos)

    def collision(self, other_organism):
        self._world.add_world_event(f'{other_organism.name} zjadl {self.name}')
        self._world.move_organism(other_organism, self.position)
        self._world.kill_organism(self)
