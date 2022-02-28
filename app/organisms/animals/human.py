from .animal import Animal
from ...utilities import OrganismType, Directions, FieldState
import pygame
import copy
from random import randint


class Human(Animal):
    def __init__(self, world, pos_x: int, pos_y: int):
        super().__init__(world, pos_x, pos_y, 4, 5, "human", OrganismType.HUMAN)
        image_path = Animal.ASSETS_PATH.joinpath("human.png")
        self._image = pygame.image.load(image_path)
        self._next_move_dir = None
        self._cooldown = 0
        self._special_skill_activated = False
        self._remaining_ability_uses = 0

    def action(self):
        """ Moves the human to desired position """
        if self._next_move_dir is None:
            return

        next_pos = self.get_next_position(self._next_move_dir)
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
        self._next_move_dir = None
        self._update_uses_and_cooldown()

    def get_next_position(self, desired_dir: Directions):
        """ Checks every field surrounding current position and returns
            first not border and if possible not occupied pos starting from desired_dir """
        move_len = 1
        if self._special_skill_activated:
            move_len = 2

        if self._special_skill_activated and self._remaining_ability_uses <= 2:
            if self._world.draw_truth(50):
                move_len = 1
                self._world.add_special_notific("the special skill did not work")

        tmp = copy.deepcopy(self.position)
        if desired_dir == Directions.LEFT:
            tmp.x -= move_len
        elif desired_dir == Directions.RIGHT:
            tmp.x += move_len
        elif desired_dir == Directions.TOP:
            tmp.y -= move_len
        elif desired_dir == Directions.BOTTOM:
            tmp.y += move_len

        f_state = self._world.get_field_state(tmp)
        if f_state != FieldState.BORDER:
            return tmp

        if move_len == 2:  # trying to move 1 space when special ab activated
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
                return tmp

        tmp = copy.deepcopy(self._position)
        tmp.state = FieldState.NOTAVAILABLE
        return tmp

    def activate_special_ability(self):
        if self._cooldown != 0:
            self._world.add_special_notific(f'cooldown {self._cooldown} turns!')
        else:
            self._world.add_special_notific('special skill activated!')
            self._cooldown = 10
            self._special_skill_activated = True
            self._remaining_ability_uses = 5

    def _update_uses_and_cooldown(self):
        if self._cooldown == 0:
            return
        if self._remaining_ability_uses > 0:
            self._remaining_ability_uses -= 1
        if self._cooldown > 0:
            self._cooldown -= 1
        if self._remaining_ability_uses == 0:
            self._special_skill_activated = False

    @property
    def image(self):
        return self._image

    @property
    def next_move_dir(self):
        return self._next_move_dir

    @next_move_dir.setter
    def next_move_dir(self, next):
        self._next_move_dir = next

    @property
    def special_skill_activated(self):
        return self._special_skill_activated

    @special_skill_activated.setter
    def special_skill_activated(self, skill):
        self._special_skill_activated = skill

    @property
    def remaining_ability_uses(self):
        return self._remaining_ability_uses

    @remaining_ability_uses.setter
    def remaining_ability_uses(self, uses):
        self._remaining_ability_uses = uses

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, cool):
        self._cooldown = cool

    def __str__(self):
        ret = f'{self.org_type.value} {self.position.x} {self.position.y} {self.age} {self.initiative} {self.strength}' \
               f' {int(self._special_skill_activated)} {self.cooldown} {self.remaining_ability_uses}'
        return ret