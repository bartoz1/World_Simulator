import pygame, sys
from app.world import World
from app.utilities import Options, OrganismType, Position, Directions
from pathlib import Path

MAIN_MENU_TEXT_POS = 50
MAIN_MENU_OPTIONS = ("Start game", "Load game", "Options", "Exit")


class Engine:
    BOLD_FONT = Path(__file__).parents[0].joinpath("assets").joinpath("motion-control.bold.otf")
    INFO_FONT = Path(__file__).parents[0].joinpath("assets").joinpath("CONSOLA.TTF")
    NOTHING_IMAGE = pygame.image.load(Path(__file__).parents[0].joinpath("assets").joinpath("nothing.png"))
    NOTIFI_FONT_SIZE = 30
    NOTIFI_COLOR = (255, 255, 255)
    INFO_COLOR = (255, 255, 255)
    EVENTS_BAR_COLOR = (48, 141, 70)
    EVENTS_BG_COLOR = (48, 41, 70)
    # SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500


    def __init__(self):
        self._human = None
        self._world = None
        pygame.init()
        self.screen_height = 500
        self.screen_width = 900
        self._window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self._background = pygame.image.load(Path(__file__).parents[0].joinpath("assets").joinpath("backzyl.bmp"))
        self._notification = ""
        self._map_width = 10
        self._map_height = 10
        self._info_shift = 0


    def main_menu(self):
        """ Draws main menu with options: new game, load game, options, exit """
        self._window.blit(self._background, (0, 0))
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
        self._draw_world_event()
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self._set_human_next_move(event):
                        self._info_shift = 0
                        self._world.play_round()
                        self._update_screen()
                    if event.key == pygame.K_s:
                        self._update_screen()
                    if event.key == pygame.K_x:
                        running = False
                        self.__clear_screen()
                    if event.key == pygame.K_q:
                        self._world.save_to_file()
                    if event.key == pygame.K_PAGEDOWN:
                        self._info_shift -= 1
                        self._draw_world_event()
                        pygame.display.update()
                    if event.key == pygame.K_PAGEUP:
                        self._info_shift += 1
                        self._draw_world_event()
                        pygame.display.update()

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
        position = (self.screen_width - text_w) / 2
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
        print(len(events))
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
        text_obj = font.render("ZDARZENIA", 0, Engine.INFO_COLOR)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (self.screen_width-260, -3)
        self._window.blit(text_obj, text_rect)

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
