import pygame, sys
from worldsimulator.world import World
from worldsimulator.utilities import Options, OrganismType, Position, Directions
from pathlib import Path
import os
MAIN_MENU_TEXT_POS = 50
MAIN_MENU_OPTIONS = ("Start game", "Load game", "Options", "EXIT")


class Engine:
    OPTIONS_MENU = ("MAP WIDTH", "MAP HEIGHT", "SAVE")
    BOLD_FONT = Path(__file__).parents[0].joinpath("assets").joinpath("motion-control.bold.otf")
    INFO_FONT = Path(__file__).parents[0].joinpath("assets").joinpath("CONSOLA.TTF")
    print(Path(__file__).parents[0].joinpath("assets").joinpath("nothing.png"))
    NOTHING_IMAGE = pygame.image.load(Path(__file__).parents[0].joinpath("assets").joinpath("nothing.png"))
    NOTIFI_FONT_SIZE = 30
    NOTIFI_COLOR = (255, 255, 255)
    INFO_COLOR = (255, 255, 255)
    EVENTS_BAR_COLOR = (48, 141, 70)
    EVENTS_BG_COLOR = (48, 41, 70)

    def __init__(self):
        self._human = None
        self._world = None
        pygame.init()
        self.screen_height = 500
        self.screen_width = 900
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)
        pygame.display.set_caption("World Symulator | Bartosz Zylwis")
        self._window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self._background = pygame.image.load(Path(__file__).parents[0].joinpath("assets").joinpath("backzyl.bmp"))
        self._notification = ""
        self._map_width = 10
        self._map_height = 10
        self._info_shift = 0

    def main_menu(self):
        """ Draws main menu with options: new game, load game, options, exit """
        self.__clear_screen()
        self._window.blit(self._background, (self.screen_width - self._background.get_width(), self.screen_height-self._background.get_height()))

        pygame.display.update()
        selected = 0
        while True:
            for i, opt in enumerate(MAIN_MENU_OPTIONS):
                if i == selected:
                    self.__draw_text(opt, (200, 134, 100), 50, MAIN_MENU_TEXT_POS*(i+1) + 20*i)
                else:
                    self.__draw_text(opt, (100, 134, 100), 50, MAIN_MENU_TEXT_POS * (i + 1) + 20*i)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if selected < len(MAIN_MENU_OPTIONS)-1:
                            selected += 1
                    if event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    if event.key == pygame.K_RETURN:
                        return Options(selected)

    def start_new_game(self):
        """ Creates new world with random organisms and draws it on the screen """
        self.__clear_screen()
        self.__generate_new_world()
        self._world.generate_organisms()
        self._human = self._world.add_human()
        self.__draw_world()

    def run_game_loop(self):

        self._update_screen()

        running = True
        while running:
            if not self._human.is_alive:
                self._game_over_info();
                running = False
                self.__clear_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self._set_human_next_move(event):    # handle human events
                        self._info_shift = 0
                        self._world.play_round()
                        self._update_screen()
                    if event.key == pygame.K_s:
                        self._update_screen()
                    if event.key == pygame.K_x:             # go back to main menu
                        running = False
                        self.__clear_screen()
                    if event.key == pygame.K_e:             # save world
                        self._world.save_to_file()
                        self._draw_save_button(0)
                    if event.key == pygame.K_PAGEDOWN:      # shift events list
                        self._info_shift -= 1
                        self._draw_world_event()
                        pygame.display.update()
                    if event.key == pygame.K_PAGEUP:        # shift events list
                        self._info_shift += 1
                        self._draw_world_event()
                        pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._scroll_info(event)
                    self._handle_mouse_click(event)
                    self._update_screen()

    def _scroll_info(self, event):
        cx, cy = event.pos  # interaction pos
        if cx > self.screen_width - 320:
            if event.button == 4:
                self._info_shift += 1
            if event.button == 5:
                self._info_shift -= 1

    def _game_over_info(self):
        self._notification = 'Game Over, human died!'
        self._draw_notification()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

    def __generate_new_world(self):
        #TODO wczytanie od uzytkownika wymiarow swiata
        self._world = World(self._map_width, self._map_height)

    def _update_screen(self):
        self.__clear_screen()
        if self._world is not None:
            self._load_notification()
        if self._notification != "":
            self._draw_notification()
        self._draw_world_event()
        self.__draw_world()
        self._draw_save_button()
        pygame.display.update()

    def __draw_world(self):
        for ri, row in enumerate(self._world.world_map):
            for ti, tile in enumerate(row):
                if tile is not None:
                    self.__draw_image(tile.image, (ti+1)*35, (ri+1)*35)
                else:
                    self.__draw_image(Engine.NOTHING_IMAGE, (ti+1)*35, (ri+1)*35)

    # draws given text-string on x,y position
    def __draw_text(self, text, color, pos_x, pos_y):
        font = pygame.font.Font(Engine.BOLD_FONT, 55)
        text_obj = font.render(text, 0, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (pos_x, pos_y)
        self._window.blit(text_obj, text_rect)
        pygame.display.update()

    # fills screen with solid color
    def __clear_screen(self):
        self._window.fill((0, 0, 0))
        # self.background = pygame.image.load("assets/backzyl.bmp")
        # self._window.blit(self.background, (0,0))

    def _set_human_next_move(self, event):
        if event.key == pygame.K_DOWN:
            self._human.next_move_dir = Directions.BOTTOM
            return True
        elif event.key == pygame.K_LEFT:
            self._human.next_move_dir = Directions.LEFT
            return True
        elif event.key == pygame.K_UP:
            self._human.next_move_dir = Directions.TOP
            return True
        elif event.key == pygame.K_RIGHT:
            self._human.next_move_dir = Directions.RIGHT
            return True
        if event.key == pygame.K_s:
            self._human.activate_special_ability()
        return False

    def __draw_rect(self, x, y):
        pygame.draw.rect(self._window, (150, 150, 150), pygame.Rect(x, y, 30, 30))

    def __draw_image(self, image, x, y):
        self._window.blit(image, (x, y))

    def _load_notification(self):
        self._notification = self._world.notification

    def _draw_notification(self):
        font = pygame.font.Font(Engine.BOLD_FONT, Engine.NOTIFI_FONT_SIZE)
        text_w, text_h = font.size(self._notification)
        position = (self.screen_width - text_w - 305) / 2
        text_obj = font.render(self._notification, 0, Engine.NOTIFI_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (position, 0)

        pygame.draw.rect(self._window, (48, 141, 70), pygame.Rect(
            position-10, -20, text_w + 20, text_h+25), 0, 3)
        self._window.blit(text_obj, text_rect)
        pygame.display.update()

    def _draw_world_event(self):
        pos_x = self.screen_width - 305
        pygame.draw.rect(self._window, Engine.EVENTS_BG_COLOR, pygame.Rect(
            pos_x-15, 0, 350, self.screen_height), 0, 0)
        pos_y = 20
        events = self._world.world_events
        self._draw_info_bar()
        if len(events) == 0:
            return
        font = pygame.font.Font(Engine.INFO_FONT, 16)
        text = events[0]
        events_splited = []
        for event in events:
            text_w, text_h = font.size(event)
            if text_w > 300:
                left, right = self.split_text(event)
                events_splited.append(left)
                events_splited.append(right)
            else:
                events_splited.append(event)

        for i, event in enumerate(events_splited):
            if i >= self._info_shift:
                text_obj = font.render(event, 0, Engine.INFO_COLOR)
                text_rect = text_obj.get_rect()
                text_rect.topleft = (pos_x, pos_y*(i-self._info_shift) + 58)
                self._window.blit(text_obj, text_rect)

    def _draw_info_bar(self):
        """ Draws a bar for world events """
        pygame.draw.rect(self._window, Engine.EVENTS_BAR_COLOR, pygame.Rect(
            self.screen_width-320, -20, 320, 70), 0, 15)
        font = pygame.font.Font(Engine.BOLD_FONT, 55)
        text_obj = font.render("EVENTS", 0, Engine.INFO_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (self.screen_width-230, -3)
        self._window.blit(text_obj, text_rect)

    def _draw_save_button(self, mode=1):
        """ Draws a button for saving game """
        if mode == 1:
            text = "SAVE THE GAME [ E ]"
            dx = 0
        else:
            text = " SAVED"
            dx = 60
        font = pygame.font.Font(Engine.BOLD_FONT, Engine.NOTIFI_FONT_SIZE)
        text_w, text_h = font.size("SAVE THE GAME [ E ]")
        position = (self.screen_width - text_w - 305) / 2
        text_obj = font.render(text, 0, Engine.NOTIFI_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (position +dx, self.screen_height - 35)

        pygame.draw.rect(self._window, (48, 141, 70), pygame.Rect(
            position - 10, self.screen_height - 40, text_w + 20, text_h + 25), 0, 9)
        self._window.blit(text_obj, text_rect)
        pygame.display.update()

    @staticmethod
    def split_text(text):
        tmp = text.split()
        left = []
        right = []
        mid = len(tmp)/2
        for i, chunk in enumerate(tmp):
            if i < mid:
                left.append(chunk)
            else:
                right.append(chunk)
        left.append('->')
        return ' '.join(left), ' '.join(right)

    def load_from_file(self):
        f = open("save.txt", "r")

        for i, line in enumerate(f):
            data = line.strip().split()
            if i == 0:
                self._world = World(int(data[0]), int(data[1]))
                self._world.round = int(data[2])
                self._map_width, self._map_height = int(data[0]), int(data[1])
            else:
                new_org = self._world.add_organism(OrganismType(int(data[0])), Position(int(data[1]), int(data[2])))
                new_org.age = int(data[3])
                new_org.initiative = int(data[4])
                new_org.strength = int(data[5])
                if OrganismType(int(data[0])) == OrganismType.HUMAN:
                    self._human = new_org
                    self._human.special_skill_activated = bool(int(data[6]))
                    self._human.cooldown = int(data[7])
                    self._human.remaining_ability_uses = int(data[8])

        self._world.update_organism_list()
        f.close()
        self._resize_window_to_map_size()

    def options_menu(self):
        """ Draws options menu with options to change: map width, map height"""
        self.__clear_screen()
        self._window.blit(self._background, (self.screen_width - self._background.get_width(), self.screen_height-self._background.get_height()))
        pygame.display.update()
        selected = 0
        while True:
            for i, opt in enumerate(Engine.OPTIONS_MENU):
                if i == selected:
                    self.__draw_text(opt, (200, 134, 100), 50, MAIN_MENU_TEXT_POS * (i + 1) + 20 * i)
                    if i==0:
                        self._draw_value_for_change(self._map_width, 5, 30, (200, 134, 100), 400 + 50,
                                                    MAIN_MENU_TEXT_POS * (i + 1) + 20 * i)
                    if i==1:
                        self._draw_value_for_change(self._map_height, 5, 25, (200, 134, 100), 400 + 50,
                                                    MAIN_MENU_TEXT_POS * (i + 1) + 20 * i)
                else:
                    self.__draw_text(opt, (100, 134, 100), 50, MAIN_MENU_TEXT_POS * (i + 1) + 20 * i)
                    if i==0:
                        self._draw_value_for_change(self._map_width, 5, 30, (100, 134, 100), 400 + 50,
                                                    MAIN_MENU_TEXT_POS * (i + 1) + 20 * i)
                    if i==1:
                        self._draw_value_for_change(self._map_height, 5, 25, (100, 134, 100), 400 + 50,
                                                    MAIN_MENU_TEXT_POS * (i + 1) + 20 * i)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if selected < len(Engine.OPTIONS_MENU) - 1:
                            selected += 1
                    if event.key == pygame.K_UP:
                        if selected > 0:
                            selected -= 1
                    if event.key == pygame.K_RIGHT:
                        if selected == 0 and 5<=self._map_width<30:
                            self._map_width += 1
                        if selected == 1 and 5<=self._map_height<25:
                            self._map_height += 1
                    if event.key == pygame.K_LEFT:
                        if selected == 0 and 5<self._map_width<=30:
                            self._map_width -= 1
                        if selected == 1 and 5<self._map_height<=25:
                            self._map_height -= 1
                    if event.key == pygame.K_RETURN and selected == 2:
                        self._resize_window_to_map_size()
                        return

    def _resize_window_to_map_size(self):
        if self._map_width <= 10:
            self.screen_width = 900
        else:
            self.screen_width = self._map_width*35 + 400

        if self._map_height <= 10:
            self.screen_height = 500
        else:
            self.screen_height = self._map_height*35 + 105

        self._window = pygame.display.set_mode((self.screen_width, self.screen_height))

    def _draw_value_for_change(self, value, min_v, max_v, color, pos_x, pos_y):
        pygame.draw.rect(self._window, (0, 0, 0), pygame.Rect(pos_x, pos_y, 150, 50))
        if value == min_v:
            text = "   "+str(value) + " >"
        elif value == max_v:
            text = "< " + str(value)
        else:
            text = "< " + str(value) + " >"
        self.__draw_text(text, color, pos_x, pos_y)

    def _map_pos_from_mouse_pos(self, m_x, m_y):
        x = m_x // 35 - 1
        y = m_y // 35 - 1
        if x < 0 or y < 0 or x >= self._map_width or y >= self._map_height:
            return Position(-1, -1)
        return Position(x, y)

    def _handle_mouse_click(self, event):
        pos = self._map_pos_from_mouse_pos(*event.pos)
        if pos.x == -1 or pos.y == -1:
            return
        x, y = event.pos
        if y+280 > self.screen_height:  # shifting y when out of screen
            y += self.screen_height - (y+280)
        self._draw_add_organism_menu(x, y)
        waiting = True
        selected = -1
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cx, cy = event.pos      # where users clicked
                    if x < cx < x + 220 and y < cy < y + 280:   # click withing the menu
                        if selected == (cy-50-y)//20+1:         # 2nd click on same organism
                            waiting = False
                            break
                        self._draw_add_organism_menu(x, y, (cy-50-y)//20+1)
                        selected = (cy-50-y)//20+1
                    else:       # click outside the menu
                        return
        self._world.add_organism(OrganismType(selected), pos)
        self._world.update_organism_list()

    def _draw_add_organism_menu(self, x, y, selected=-1):
        graphics = ["assets/wolf.png", "assets/sheep.png", "assets/fox.png", "assets/turtle.png", "assets/antelope.png", "assets/grass.png", "assets/dandelion.png", "assets/guarana.png", "assets/wolf_berries.png", "assets/hogweed.png", "assets/cybersheep.png"]
        pygame.draw.rect(self._window, Engine.EVENTS_BG_COLOR, pygame.Rect(
            x, y, 200, 280), 0, 15)
        pygame.draw.rect(self._window, Engine.EVENTS_BAR_COLOR, pygame.Rect(
            x, y, 200, 40), 0, 15)
        pygame.draw.rect(self._window, Engine.EVENTS_BAR_COLOR, pygame.Rect(
            x, y, 200, 280), 3, 15)
        font = pygame.font.Font(Engine.BOLD_FONT, 35)
        text_obj = font.render("ADD ORGANISM", 0, Engine.INFO_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x+10, y)
        self._window.blit(text_obj, text_rect)
        font = pygame.font.Font(Engine.INFO_FONT, 15)

        for i, organism in enumerate(OrganismType):     # listing all available organisms
            if organism != OrganismType.HUMAN:
                if selected == i:
                    text_obj = font.render(organism.name, 0, Engine.EVENTS_BAR_COLOR)
                else:
                    text_obj = font.render(organism.name, 0, Engine.INFO_COLOR)
                text_rect = text_obj.get_rect()
                text_rect.topleft = (x+55, y+10+ (i + 1)*20)

                graphic = pygame.transform.scale(pygame.image.load("app\\"+graphics[i-1]), (20, 20))
                self.__draw_image(graphic, x+30, y+5+ (i + 1)*20)
                self._window.blit(text_obj, text_rect)
        pygame.display.update()


