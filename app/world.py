from app.utilities import Position, FieldState, OrganismType
import bisect
from random import randint
from app.organisms.animals.wolf import Wolf
from app.organisms.animals.sheep import Sheep
from app.organisms.animals.animal import Animal
#from organisms.organism import Organism
from pprint import pprint


class World:
    def __init__(self, m_width, m_height):
        self._world_height = m_height
        self._world_width = m_width
        self.world_map =[[None for j in range(m_width)] for i in range(m_height)]
        self._world_events = set()
        self._organism_list = []
        self._born_organism_list = []
        self._round = 0;
        print(self.world_map)

    def get_field_state(self, position: Position):
        if position.y >= self._world_height or position.y < 0 or position.x < 0 or position.x >= self._world_width:
            position.state = FieldState.BORDER
        elif self.world_map[position.y][position.x] is None:
            position.state = FieldState.AVAILABLE
        else:
            position.state = FieldState.OCCUPIED
        return position.state

    def add_world_event(self, event: str):
        self._world_events.add(event)

    def get_organism_by_pos(self, position: Position):
        return self.world_map[position.y][position.x]

    def play_round(self):
        print("runda!")
        # pprint(self.world_map)
        #pprint(self._organism_list)
        for organism in self._organism_list:
            organism.action()
        self._round += 1
        self._update_organism_list()
        print(str(self._world_events))

    def move_organism(self, organism, next_pos: Position):
        """ moves organism from current position on map to next_pos (making previous posision None on map)"""
        self._clear_position(organism.position)
        self.world_map[next_pos.y][next_pos.x] = organism
        organism.position = next_pos
        pprint(self.world_map)

    def _clear_position(self, position: Position):
        self.world_map[position.y][position.x] = None

    def kill_organism(self, organism):
        if self.world_map[organism.position.y][organism.position.x] == organism:
            self.world_map[organism.position.y][organism.position.x] = None
        organism.set_death()

    @staticmethod
    def are_diferent_positions(pos1: Position, pos2: Position):
        if pos1.x == pos2.x and pos1.y == pos2.y:
            return False
        return True

    def add_organism(self, organism_type: OrganismType, position: Position):
        # TODO ify dla kazdego rodzaju zwierzecia
        new_organism = None
        if organism_type == OrganismType.WOLF:
            new_organism = Wolf(self, position.x, position.y)
        elif organism_type == OrganismType.SHEEP:
            new_organism = Sheep(self, position.x, position.y)

        self._born_organism_list.append(new_organism)
        self.world_map[position.y][position.x] = new_organism

    def _update_organism_list(self):
        self._organism_list = [org for org in self._organism_list if org.is_alive]              # removes dead organisms
        self._born_organism_list = [org for org in self._born_organism_list if org.is_alive]    # removes dead organisms
        for org in self._born_organism_list:
            bisect.insort(self._organism_list, org)
        self._born_organism_list = []

    @staticmethod
    def draw_truth( percent: int) -> bool:
        """ True or False generator with posibility given as param (0 - 100) """
        if randint(1, 100) <= percent:
            return True
        return False

    def get_random_available_position(self):
        """ gets available position from map - choosing randomly, tries 150 times"""
        tmp:Position
        for i in range(150):
            tmp.x = randint(0, self._world_width-1)
            tmp.y = randint(0, self._world_height)
            if self.get_field_state(tmp) == FieldState.AVAILABLE:
                return tmp
        return Position(0, 0, FieldState.NOTAVAILABLE)

    def generate_organisms(self):
        self.add_organism(OrganismType.WOLF, Position(4, 2))
        self.add_organism(OrganismType.SHEEP, Position(2, 2))
        self._update_organism_list()


