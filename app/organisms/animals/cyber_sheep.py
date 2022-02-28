from .animal import Animal
from app.utilities import OrganismType, Position, Directions, FieldState
import pygame
import math
import copy

class CyberSheep(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 4, 11, "cybersheep", OrganismType.CYBER_SHEEP)
        image_path = Animal.ASSETS_PATH.joinpath("cybersheep.png")
        self._image = pygame.image.load(image_path)

    def action(self):
        """ Cyber Sheep tries to exterminate hogweed - finds the closest and goes there but if
            there is no hogweed on the map than acts just like a normal sheep"""
        hogweed_list = self._world.get_hogweed()

        if len(hogweed_list) == 0:   # no hogweed on the map
            super().action()
            return

        min_len = self._count_distance(self.position, hogweed_list[0].position)
        min_id = 0
        for i, hw in enumerate(hogweed_list):
            tmp_len = self._count_distance(self.position, hw.position)

            if tmp_len < min_len:
                min_len = tmp_len
                min_id = i
        next_pos = self._next_pos_by_destination(hogweed_list[min_id].position)

        if next_pos.state == FieldState.NOTAVAILABLE:                           # no available moves
            self._world.add_world_event(f'{self.name} cannot move')
        elif next_pos.state == FieldState.OCCUPIED:                             # collision with other organism
            other_organism = self._world.get_organism_by_pos(next_pos)
            other_organism.collision(self)
        elif next_pos.state == FieldState.AVAILABLE:                            # moves to available position
            self._world.add_world_event(f'{self.name} moved to: ({next_pos.x}, {next_pos.y})')
            self._world.move_organism(self, next_pos)
        else:
            self._world.add_world_event(f'{self.name} sleeps')

    def _next_pos_by_destination(self, dest_pos: Position):
        if self.position.x == dest_pos:
            return dest_pos
        angle = self._angle(dest_pos, self.position)
        next_p = Directions.LEFT
        if 45 >= angle >= 0 or 315 <= angle < 360:
            next_p = Directions.RIGHT
        if 135 >= angle > 45:
            next_p = Directions.BOTTOM    # intuicyjnie top ale ze wzgledu na mape bottom
        if 225 >= angle > 135:
            next_p = Directions.LEFT
        if 315 >= angle > 225:
            next_p = Directions.TOP       # intuicyjnie bottom ale ze wzgledu na mape top

        tmp = copy.deepcopy(self._position)
        if next_p == Directions.LEFT:
            tmp.x -= 1
        elif next_p == Directions.RIGHT:
            tmp.x += 1
        elif next_p == Directions.TOP:
            tmp.y -= 1
        elif next_p == Directions.BOTTOM:
            tmp.y += 1
        if self._world.get_field_state(tmp) != FieldState.BORDER:
            return tmp
        return copy.deepcopy(self._position)


    @staticmethod
    def _count_distance( pos1: Position, pos2: Position):
        return math.sqrt(math.pow(pos2.x-pos1.x, 2) + math.pow(pos2.y-pos1.y, 2))

    @staticmethod
    def _angle(a, b):
        ang = math.degrees(math.atan2(a.y-b.y, a.x-b.x))
        return ang + 360 if ang < 0 else ang

    @property
    def image(self):
        return self._image