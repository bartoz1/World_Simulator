import pygame, sys
from app.world import World
from app.utilities import Options, OrganismType, Position, Directions
from pathlib import Path

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
MAIN_MENU_TEXT_POS = 50
MAIN_MENU_OPTIONS = ("Start game", "Load game", "Options", "Exit")

class Engine:
    def __init__(self):
        self._human = None
        self._world = None
        pygame.init()
        self._window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._background = pygame.image.load(Path(__file__).parents[0].joinpath("assets").joinpath("backzyl.bmp"))

    # Main menu - new game, load game, options, exit
    def main_menu(self):
        """ Draws main menu with options: new game, load game, options, exit """
        self._window.blit(self._background, (0, 0))
        pygame.display.update()
        selected = 0
        while True:
            for i, opt in enumerate(MAIN_MENU_OPTIONS):
                if i == selected:
                    self.__draw_text(opt, (200, 134, 100), 50, MAIN_MENU_TEXT_POS*(i+1))
                else:
                    self.__draw_text(opt, (100, 134, 100), 50, MAIN_MENU_TEXT_POS * (i + 1))

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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self._set_human_next_move(event):
                        self._world.play_round()
                        self.__clear_screen()
                        self.__draw_world()
                    if event.key == pygame.K_x:
                        running = False

    def __generate_new_world(self):
        #TODO wczytanie od uzytkownika wymiarow swiata
        self._world = World(10, 10)

    def __draw_world(self):
        for ri, row in enumerate(self._world.world_map):
            for ti, tile in enumerate(row):
                if tile is not None:
                    self.__draw_image(tile.image, (ti+1)*35, (ri+1)*35)
                else:
                    self.__draw_rect((ti+1)*35, (ri+1)*35)
        pygame.display.update()

    # draws given text-string on x,y position
    def __draw_text(self, text, color, pos_x, pos_y):
        font = pygame.font.SysFont(None, 35)
        textObj = font.render(text, 0, color)
        textRect = textObj.get_rect()
        textRect.topleft = (pos_x, pos_y)
        self._window.blit(textObj, textRect)
        pygame.display.update()

    # fills screen with solid color
    def __clear_screen(self):
        self._window.fill((0, 0, 0))
        self.background = pygame.image.load("assets/backzyl.bmp")
        self._window.blit(self.background, (0,0))

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