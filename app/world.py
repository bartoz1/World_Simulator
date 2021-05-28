from app.utilities import Position, FieldState, OrganismType
import bisect
from random import randint
from app.organisms.animals.wolf import Wolf
from app.organisms.animals.sheep import Sheep
from app.organisms.animals.cyber_sheep import CyberSheep
from app.organisms.animals.fox import Fox
from app.organisms.animals.antelope import Antelope
from app.organisms.animals.turtle import Turtle
from app.organisms.animals.human import Human
from app.organisms.plants.grass import Grass
from app.organisms.plants.dandelion import Dandelion
from app.organisms.plants.wolfberries import WolfBerries
from app.organisms.plants.guarana import Guarana
from app.organisms.plants.hogweed import Hogweed
import copy

from app.organisms.animals.animal import Animal
#from organisms.organism import Organism
from pprint import pprint


class World:
    ORGANISMS_DENSITY = 0.1

    def __init__(self, m_width, m_height):
        self._world_height = m_height
        self._world_width = m_width
        self.world_map =[[None for j in range(m_width)] for i in range(m_height)]
        self._world_events = []
        self._organism_list = []
        self._born_organism_list = []
        self._round = 0
        self._notification = ""

    def get_field_state(self, position: Position):
        if position.y >= self._world_height or position.y < 0 or position.x < 0 or position.x >= self._world_width:
            position.state = FieldState.BORDER
        elif self.world_map[position.y][position.x] is None:
            position.state = FieldState.AVAILABLE
        else:
            position.state = FieldState.OCCUPIED
        return position.state

    def add_world_event(self, event: str):
        # self._world_events.add(event)
        self._world_events.append(event)

    def get_organism_by_pos(self, position: Position):
        return self.world_map[position.y][position.x]

    def play_round(self):
        self._world_events = []
        for organism in self._organism_list:
            if organism.is_alive:
                organism.age += 1
                # print(f'{organism.name} str: {organism.strength}')
                organism.action()
        self._round += 1
        self.update_organism_list()


    def move_organism(self, organism, next_pos: Position):
        """ moves organism from current position on map to next_pos (making previous posision None on map)"""
        self._clear_position(organism.position)
        self.world_map[next_pos.y][next_pos.x] = organism
        organism.position = next_pos

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
        elif organism_type == OrganismType.CYBER_SHEEP:
            new_organism = CyberSheep(self, position.x, position.y)
        elif organism_type == OrganismType.FOX:
            new_organism = Fox(self, position.x, position.y)
        elif organism_type == OrganismType.ANTELOPE:
            new_organism = Antelope(self, position.x, position.y)
        elif organism_type == OrganismType.HUMAN:
            new_organism = Human(self, position.x, position.y)
        elif organism_type == OrganismType.TURTLE:
            new_organism = Turtle(self, position.x, position.y)
        elif organism_type == OrganismType.GRASS:
            new_organism = Grass(self, position.x, position.y)
        elif organism_type == OrganismType.DANDELION:
            new_organism = Dandelion(self, position.x, position.y)
        elif organism_type == OrganismType.WOLF_BERRIES:
            new_organism = WolfBerries(self, position.x, position.y)
        elif organism_type == OrganismType.GUARANA:
            new_organism = Guarana(self, position.x, position.y)
        elif organism_type == OrganismType.HOGWEED:
            new_organism = Hogweed(self, position.x, position.y)

        self._born_organism_list.append(new_organism)
        self.world_map[position.y][position.x] = new_organism

        return new_organism

    def update_organism_list(self):
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
        tmp = Position(-1, -1)
        for i in range(150):
            tmp.x = randint(0, self._world_width-1)
            tmp.y = randint(0, self._world_height-1)
            if self.get_field_state(tmp) == FieldState.AVAILABLE:
                return tmp
        return Position(0, 0, FieldState.NOTAVAILABLE)

    def generate_organisms(self):
        for org_type in OrganismType:
            org_count = 2
            org_count += randint(0, 1 + int((self._world_width * self._world_height) / 11 * World.ORGANISMS_DENSITY))
            if org_type == OrganismType.HUMAN:
                org_count = 0

            for i in range(org_count):
                position = self.get_random_available_position()
                if position.state == FieldState.NOTAVAILABLE:
                    break
                self.add_organism(org_type, position)

        self.update_organism_list()

    def add_human(self):
        pos = self.get_random_available_position()
        human = Human(self, pos.x, pos.y)
        self.world_map[pos.y][pos.x] = human
        self._born_organism_list.append(human)
        self.update_organism_list()
        return human

    def get_hogweed(self):
        lista = []
        for org in self._organism_list:
            if org.org_type == OrganismType.HOGWEED:
                lista.append(org)
        return lista

    def add_special_notific(self, text: str):
        self._notification = text

    def save_to_file(self):
        f = open("save.txt", "w")
        f.write(f'{self._world_width} {self._world_height} {self._round}\n')
        for org in self._organism_list:
            f.write(str(org))
            f.write('\n')

        f.close()

    @property
    def notification(self):
        ret = copy.deepcopy(self._notification)
        self._notification = ""
        return ret

    @property
    def world_events(self):
        return self._world_events

    @world_events.setter
    def world_events(self, new):
        self._world_events = new

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, new_round):
        self._round = new_round
